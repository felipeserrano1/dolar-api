package main

import (
	"api-dolar2/controllers"
	"api-dolar2/initializers"
	"fmt"
	"github.com/gin-gonic/gin"
)

func init() {
	initializers.LoadEnvVariables()
	initializers.ConnectToDB()
}

func main() {
	fmt.Println("hello world")
	r := gin.Default()
	r.GET("/valores", controllers.GetAll)
	r.Run()
}
