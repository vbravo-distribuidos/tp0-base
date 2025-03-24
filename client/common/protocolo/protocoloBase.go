package protocolo

import (
	"encoding/binary"
	"net"
)

const TAMANIO_UINT32 = 4

func recibirBytes(conn net.Conn, largo uint32) ([]byte, error) {
	bytes := make([]byte, largo)
	bytes_recibidos := uint32(0)

	for bytes_recibidos < largo {
		n, err := conn.Read(bytes[bytes_recibidos:])
		bytes_recibidos += uint32(n)
		if err != nil {
			return bytes, err
		}
	}

	return bytes, nil
}

func recibirEnteroU32(conn net.Conn) (uint32, error) {
	bytes, err := recibirBytes(conn, TAMANIO_UINT32)
	if err != nil {
		return 0, err
	}
	return binary.BigEndian.Uint32(bytes), nil
}

func recibirString(conn net.Conn) (string, error) {
	largo, err := recibirEnteroU32(conn)
	if err != nil {
		return "", err
	}

	bytes, err := recibirBytes(conn, largo)
	if err != nil {
		return "", err
	}

	return string(bytes), nil
}

func enviarBytes(conn net.Conn, msg []byte) (int, error) {
	largo := len(msg)
	bytes_enviados := 0

	for bytes_enviados < largo {
		n, err := conn.Write(msg[bytes_enviados:])
		bytes_enviados += n
		if err != nil {
			return bytes_enviados, err
		}
	}

	return bytes_enviados, nil
}

func enviarEnteroU32(conn net.Conn, entero uint32) (int, error) {
	bytes := make([]byte, TAMANIO_UINT32)
	binary.BigEndian.PutUint32(bytes, entero)
	return enviarBytes(conn, bytes)
}

func enviarString(conn net.Conn, texto string) (int, error) {
	bytes := []byte(texto)
	n, err := enviarEnteroU32(conn, uint32(len(bytes)))
	if err != nil {
		return n, err
	}

	return enviarBytes(conn, bytes)
}
