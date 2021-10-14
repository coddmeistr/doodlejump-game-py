package main

import (
	"context"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
)

var router *gin.Engine

var collEmployees *mongo.Collection
var collDepartments *mongo.Collection
var ctx = context.TODO()


func main(){
	// Create client
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://127.0.0.1:27017"))
	if err != nil {
		log.Fatal(err)
	}

	// Create connect
	err = client.Connect(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}


	// choosing base root collections
	collEmployees = client.Database("Base").Collection("Employees")
	collDepartments = client.Database("Base").Collection("Departments")

	base := NewBase()
	handler := NewHandler(base)

	router = gin.Default()

	router.POST("/employee", handler.CreateEmployee)
	router.GET("/employee/:id", handler.GetEmployee)
	//router.PUT("/employee/:id", handler.UpdateEmployee)
	//router.DELETE("/employee/:id", handler.DeleteEmployee)

	router.Run()
}





