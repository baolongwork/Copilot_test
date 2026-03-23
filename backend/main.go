package main

import (
	"crypto/rand"
	"encoding/hex"
	"net/http"
	"strconv"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

const (
	sessionTTL      = 24 * time.Hour
	minPasswordLen  = 8
)

type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	Password  string    `json:"-"`
	CreatedAt time.Time `json:"created_at"`
}

type Product struct {
	ID          int       `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Price       float64   `json:"price"`
	CreatedAt   time.Time `json:"created_at"`
}

type session struct {
	userID    int
	expiresAt time.Time
}

const resetTokenTTL = 1 * time.Hour

type resetToken struct {
	userID    int
	expiresAt time.Time
}

var (
	users      []User
	products   []Product
	userMu     sync.RWMutex
	productMu  sync.RWMutex
	userNextID = 1
	prodNextID = 1

	sessions  = map[string]session{}
	sessionMu sync.RWMutex

	resetTokens  = map[string]resetToken{}
	resetTokenMu sync.Mutex
)

func generateToken() (string, error) {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}

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

	// Auth routes
	api.POST("/login", loginHandler)
	api.POST("/logout", logoutHandler)
	api.POST("/forgot-password", forgotPasswordHandler)
	api.POST("/reset-password", resetPasswordHandler)

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
		Name     string `json:"name" binding:"required"`
		Email    string `json:"email" binding:"required"`
		Password string `json:"password"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if len(input.Password) > 0 && len(input.Password) < minPasswordLen {
		c.JSON(http.StatusBadRequest, gin.H{"error": "password must be at least 8 characters"})
		return
	}
	hashedPassword := ""
	if input.Password != "" {
		hash, err := bcrypt.GenerateFromPassword([]byte(input.Password), bcrypt.DefaultCost)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "could not hash password"})
			return
		}
		hashedPassword = string(hash)
	}
	userMu.Lock()
	defer userMu.Unlock()
	u := User{ID: userNextID, Name: input.Name, Email: input.Email, Password: hashedPassword, CreatedAt: time.Now()}
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
		Description *string  `json:"description"`
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
			if input.Description != nil {
				products[i].Description = *input.Description
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

// Auth handlers
func loginHandler(c *gin.Context) {
	var input struct {
		Email    string `json:"email" binding:"required"`
		Password string `json:"password" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	userMu.RLock()
	var matched *User
	for i := range users {
		if users[i].Email == input.Email {
			matched = &users[i]
			break
		}
	}
	userMu.RUnlock()
	if matched == nil || bcrypt.CompareHashAndPassword([]byte(matched.Password), []byte(input.Password)) != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid email or password"})
		return
	}
	token, err := generateToken()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not generate session token"})
		return
	}
	sessionMu.Lock()
	sessions[token] = session{userID: matched.ID, expiresAt: time.Now().Add(sessionTTL)}
	sessionMu.Unlock()
	c.JSON(http.StatusOK, gin.H{"token": token, "user": matched})
}

func logoutHandler(c *gin.Context) {
	token := c.GetHeader("Authorization")
	if token == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "missing Authorization header"})
		return
	}
	sessionMu.Lock()
	delete(sessions, token)
	sessionMu.Unlock()
	c.JSON(http.StatusOK, gin.H{"message": "logged out"})
}

func forgotPasswordHandler(c *gin.Context) {
	var input struct {
		Email string `json:"email" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	userMu.RLock()
	var matched *User
	for i := range users {
		if users[i].Email == input.Email {
			matched = &users[i]
			break
		}
	}
	userMu.RUnlock()
	// Always respond with success to avoid user enumeration
	if matched == nil {
		c.JSON(http.StatusOK, gin.H{"message": "If that email is registered, a reset token has been sent."})
		return
	}
	token, err := generateToken()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not generate reset token"})
		return
	}
	resetTokenMu.Lock()
	resetTokens[token] = resetToken{userID: matched.ID, expiresAt: time.Now().Add(resetTokenTTL)}
	resetTokenMu.Unlock()
	// In a real application the token would be emailed; here we return it directly for demo purposes.
	c.JSON(http.StatusOK, gin.H{"message": "If that email is registered, a reset token has been sent.", "reset_token": token})
}

func resetPasswordHandler(c *gin.Context) {
	var input struct {
		Token    string `json:"token" binding:"required"`
		Password string `json:"password" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if len(input.Password) < minPasswordLen {
		c.JSON(http.StatusBadRequest, gin.H{"error": "password must be at least 8 characters"})
		return
	}
	resetTokenMu.Lock()
	rt, ok := resetTokens[input.Token]
	if ok {
		delete(resetTokens, input.Token)
	}
	resetTokenMu.Unlock()
	if !ok || time.Now().After(rt.expiresAt) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid or expired reset token"})
		return
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(input.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not hash password"})
		return
	}
	userMu.Lock()
	defer userMu.Unlock()
	for i := range users {
		if users[i].ID == rt.userID {
			users[i].Password = string(hash)
			c.JSON(http.StatusOK, gin.H{"message": "password has been reset successfully"})
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
}
