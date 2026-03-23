package main

import (
	"net/http"
	"strconv"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

type Product struct {
	ID          int       `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Price       float64   `json:"price"`
	CreatedAt   time.Time `json:"created_at"`
}

var (
	users      []User
	products   []Product
	userMu     sync.RWMutex
	productMu  sync.RWMutex
	userNextID = 1
	prodNextID = 1
)

func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "http://localhost:5173")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	}
}

func main() {
	r := gin.Default()
	r.Use(corsMiddleware())

	api := r.Group("/api")

	// User routes
	api.GET("/users", getUsers)
	api.GET("/users/:id", getUserByID)
	api.POST("/users", createUser)
	api.PUT("/users/:id", updateUser)
	api.DELETE("/users/:id", deleteUser)

	// Product routes
	api.GET("/products", getProducts)
	api.GET("/products/:id", getProductByID)
	api.POST("/products", createProduct)
	api.PUT("/products/:id", updateProduct)
	api.DELETE("/products/:id", deleteProduct)

	r.Run(":8080")
}

// User handlers
func getUsers(c *gin.Context) {
	userMu.RLock()
	defer userMu.RUnlock()
	c.JSON(http.StatusOK, users)
}

func getUserByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	userMu.RLock()
	defer userMu.RUnlock()
	for _, u := range users {
		if u.ID == id {
			c.JSON(http.StatusOK, u)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
}

func createUser(c *gin.Context) {
	var input struct {
		Name  string `json:"name" binding:"required"`
		Email string `json:"email" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	userMu.Lock()
	defer userMu.Unlock()
	u := User{ID: userNextID, Name: input.Name, Email: input.Email, CreatedAt: time.Now()}
	userNextID++
	users = append(users, u)
	c.JSON(http.StatusCreated, u)
}

func updateUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	var input struct {
		Name  string `json:"name"`
		Email string `json:"email"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	userMu.Lock()
	defer userMu.Unlock()
	for i, u := range users {
		if u.ID == id {
			if input.Name != "" {
				users[i].Name = input.Name
			}
			if input.Email != "" {
				users[i].Email = input.Email
			}
			c.JSON(http.StatusOK, users[i])
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
}

func deleteUser(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	userMu.Lock()
	defer userMu.Unlock()
	for i, u := range users {
		if u.ID == id {
			users = append(users[:i], users[i+1:]...)
			c.JSON(http.StatusOK, gin.H{"message": "user deleted"})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
}

// Product handlers
func getProducts(c *gin.Context) {
	productMu.RLock()
	defer productMu.RUnlock()
	c.JSON(http.StatusOK, products)
}

func getProductByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	productMu.RLock()
	defer productMu.RUnlock()
	for _, p := range products {
		if p.ID == id {
			c.JSON(http.StatusOK, p)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "product not found"})
}

func createProduct(c *gin.Context) {
	var input struct {
		Name        string  `json:"name" binding:"required"`
		Description string  `json:"description"`
		Price       float64 `json:"price" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	productMu.Lock()
	defer productMu.Unlock()
	p := Product{ID: prodNextID, Name: input.Name, Description: input.Description, Price: input.Price, CreatedAt: time.Now()}
	prodNextID++
	products = append(products, p)
	c.JSON(http.StatusCreated, p)
}

func updateProduct(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	var input struct {
		Name        string   `json:"name"`
		Description string   `json:"description"`
		Price       *float64 `json:"price"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	productMu.Lock()
	defer productMu.Unlock()
	for i, p := range products {
		if p.ID == id {
			if input.Name != "" {
				products[i].Name = input.Name
			}
			if input.Description != "" {
				products[i].Description = input.Description
			}
			if input.Price != nil {
				products[i].Price = *input.Price
			}
			c.JSON(http.StatusOK, products[i])
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "product not found"})
}

func deleteProduct(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id"})
		return
	}
	productMu.Lock()
	defer productMu.Unlock()
	for i, p := range products {
		if p.ID == id {
			products = append(products[:i], products[i+1:]...)
			c.JSON(http.StatusOK, gin.H{"message": "product deleted"})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "product not found"})
}
