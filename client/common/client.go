package common

import (
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
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
func (c *Client) StartClientLoop(apuesta *Apuesta) {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGTERM)

	if !c.seguirCorriendo(sigs) {
		return
	}

	err := c.createClientSocket()
	if err != nil {
		return
	}

	defer c.conn.Close()

	log.Infof("action: sending_bet | result: in_progress | bet: %s", apuestaAString(apuesta))
	_, err = enviarApuesta(c.conn, apuesta)
	if err != nil {
		log.Errorf("action: send_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}
	log.Infof("action: send_message | result: success | client_id: %v", c.config.ID)

	respuesta, err := recibirRespuesta(c.conn)
	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v", c.config.ID, err)
		return
	}

	if respuesta.esOk() {
		log.Infof("action: receive_status | result: success | client_id: %v | response: %v", c.config.ID, respuesta.estado)
	} else {
		log.Errorf("action: receive_status | result: fail | client_id: %v | response: %v", c.config.ID, respuesta.estado)
	}

	// Wait a time between sending one message and the next one

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}
