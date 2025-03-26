package common

import (
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/protocolo"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/serializacion"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID             string
	ServerAddress  string
	BatchMaxAmount int
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return err
}

// seguirCorriendo Indica si el cliente deberia seguir ejecutando.
// Sigue corriendo si el ID del mensaje es menor a la cantidad indicanda en LoopAmount
// Termina si lo sobrepasó, recibio una señal del tipo SIGTERM
func (c *Client) seguirCorriendo(sigs chan os.Signal) bool {
	select {
	case <-sigs:
		log.Infof("action: signal_received | result: success")
		return false
	default:
		return true
	}
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGTERM)

	err := c.createClientSocket()
	if err != nil {
		return
	}

	nombreArchivo := fmt.Sprintf(".data/agency-%s.csv", c.config.ID)
	lectorApuestas, err := serializacion.NewLectorApuestas(nombreArchivo, c.config.ID, c.config.BatchMaxAmount)
	if err != nil {
		log.Criticalf(
			"action: create_bet_reader | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	defer c.conn.Close()
	defer lectorApuestas.Cerrar()

	for {
		if !c.seguirCorriendo(sigs) {
			listaVacia := make([]*modelo.Apuesta, 0)
			protocolo.EnviarApuestas(c.conn, listaVacia)
			break

		}

		apuestas := lectorApuestas.Leer()

		_, err := protocolo.EnviarApuestas(c.conn, apuestas)
		if err != nil {
			log.Warningf(
				"action: send_bets | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			break
		}

		if len(apuestas) == 0 {
			log.Infof(
				"action: send_bets | result: success | client_id: %v | message: no_bets",
				c.config.ID,
			)
			break
		}

		respuesta, err := protocolo.RecibirRespuesta(c.conn)
		if err != nil {
			log.Warningf(
				"action: receive_response | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			break
		}
		if respuesta.EsOk() {
			log.Infof(
				"action: receive_response | result: success | client_id: %v | response: %+v",
				c.config.ID,
				respuesta.Estado,
			)
		} else {
			log.Warningf(
				"action: receive_response | result: fail | client_id: %v | response: %+v",
				c.config.ID,
				respuesta.Estado,
			)
		}

	}

	_, err = protocolo.EnviarAgencia(c.conn, c.config.ID)
	if err != nil {
		log.Criticalf("action: envio_consulta_ganadores | result: fail | error: %v", err)
	}

	apuestasGanadoras, err := protocolo.RecibirApuestas(c.conn)
	if err != nil {
		log.Criticalf("action: consulta_ganadores | result: fail | error: %v", err)
		return
	}

	log.Infof("action: consulta_ganadores | result: success | cant_ganadores: %d", len(apuestasGanadoras))

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}
