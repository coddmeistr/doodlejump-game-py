package main

import (
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"sync"
)

type Employee struct{
	ID      int      `json:"id"`
	Name    string   `json:"name"`
	Sex     string   `json:"sex"`
	Age     int      `json:"age"`
	Salary  int      `json:"salary"`
}

type Department struct{
	ID         int        `json:"id"`
	Name       string     `json:"name"`
	Employees  []Employee `json:"employees"`
}

type Database interface {
	InsertEmployee(e Employee)
	GetEmployee(id int, employee *Employee) (Employee, error)
	//DeleteEmployee(id int)
	//CreateDepartment(d *Department)
	//GetDepartment(id int)
	//DeleteDepartment(id int)
}

type Base struct{
	collEmployees *mongo.Collection
	countEmployees int
	collDepartments *mongo.Collection
	countDepartments int
	sync.Mutex
}

func NewBase() *Base{
	return &Base{
		collEmployees:  collEmployees,
		collDepartments: collDepartments,
		countEmployees: 0,
		countDepartments: 0,
	}
}

/*func (s *MemoryStorage) LoadStorageFromCollection() int{
	var employees []*Employee

	options := options.Find()
	filter := bson.M{}

	cur, err := collection.Find(ctx, filter, options)
	if err != nil {
		log.Fatal(err)
	}

	for cur.Next(ctx) {

		// create a value into which the single document can be decoded
		var elem Employee
		err := cur.Decode(&elem)
		if err != nil {
			log.Fatal(err)
		}

		employees = append(employees, &elem)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}
	cur.Close(context.TODO())

	count := 0
	for _, e := range employees{
		s.data[e.ID] = *e
		count++
	}

	return count
}*/

func (b *Base) InsertEmployee(e Employee){
	b.countEmployees++
	e.ID = b.countEmployees
	b.collEmployees.InsertOne(ctx, e)
}

func (b *Base) GetEmployee(id int, employee *Employee) (Employee, error){
	options := options.FindOne()
	filter := bson.D{{"id", id}}
	result := b.collEmployees.FindOne(ctx, filter, options)
	result.Decode(&employee)
	if mongo.ErrNoDocuments == result.Err(){
		return *employee, result.Err()
	}
	return *employee, nil
}
