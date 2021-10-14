package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
)

type ErrorResponse struct{
	Message string `json:"message"`
}

type Handler struct{
	base Database
}

func NewHandler(base Database) *Handler{
	return &Handler{base: base}
}

func (h *Handler) CreateEmployee(c *gin.Context){
	var employee Employee

	if err := c.BindJSON(&employee); err != nil{
		fmt.Printf("failed to bind employee: %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	h.base.InsertEmployee(employee)

	/*c.JSON(http.StatusOK, map[string]interface{}{
		"id": employee.ID,
	})*/

}

/*func (h *Handler) UpdateEmployee(c *gin.Context){
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil{
		fmt.Printf("failed to convert id param to int: %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	var employee Employee

	if err := c.BindJSON(&employee); err != nil{
		fmt.Printf("failed to bind employee: %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	h.storage.Update(id, employee)

	c.JSON(http.StatusOK, map[string]interface{}{
		"id": employee.ID,
	})

}*/

func (h *Handler) GetEmployee(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		fmt.Printf("failed to convert id param to int: %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	var employee Employee
	employee, err = h.base.GetEmployee(id, &employee)
	if err != nil {
		fmt.Printf("failed to get employee %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, employee)
}

/*func (h *Handler) GetAllEmployee(c *gin.Context) {

	data := h.storage.GetAll()
	if len(data) == 0{
		c.JSON(http.StatusOK, ErrorResponse{
			Message: "No employees.",
		})
		return
	}

	for _, value := range data{
		c.JSON(http.StatusOK, value)
	}

}

func (h *Handler) DeleteEmployee(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		fmt.Printf("failed to convert id param to int: %s\n", err.Error())
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: err.Error(),
		})
		return
	}

	options := options.Delete()
	filter := bson.D{{"id", id}}

	collection.DeleteOne(ctx, filter, options)

	h.storage.Delete(id)

	c.String(http.StatusOK, "employee deleted")
}*/
