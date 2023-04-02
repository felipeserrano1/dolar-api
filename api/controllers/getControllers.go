package controllers

import (
	"api-dolar2/initializers"
	"api-dolar2/models"

	"github.com/gin-gonic/gin"
)

func GetAll(c *gin.Context) {
	var posts []models.Post
	initializers.DB.Find(&posts)

	c.JSON(200, gin.H{
		"posts": posts,
	})
}
