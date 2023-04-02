package models

import (
	"time"
)

type Post struct {
	Fecha *time.Time
	Valor float64 `gorm:"type:decimal(10,2);"`
	//Title string
	//Body  string
}
