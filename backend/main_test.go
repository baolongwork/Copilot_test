package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.Use(corsMiddleware())

	api := r.Group("/api")

	api.POST("/login", loginHandler)
	api.POST("/logout", logoutHandler)
	api.POST("/forgot-password", forgotPasswordHandler)
	api.POST("/reset-password", resetPasswordHandler)

	api.GET("/users", getUsers)
	api.GET("/users/:id", getUserByID)
	api.POST("/users", createUser)
	api.PUT("/users/:id", updateUser)
	api.DELETE("/users/:id", deleteUser)

	api.GET("/products", getProducts)
	api.GET("/products/:id", getProductByID)
	api.POST("/products", createProduct)
	api.PUT("/products/:id", updateProduct)
	api.DELETE("/products/:id", deleteProduct)

	return r
}

func resetState() {
	userMu.Lock()
	users = nil
	userNextID = 1
	userMu.Unlock()

	productMu.Lock()
	products = nil
	prodNextID = 1
	productMu.Unlock()

	sessionMu.Lock()
	sessions = map[string]session{}
	sessionMu.Unlock()

	resetTokenMu.Lock()
	resetTokens = map[string]resetToken{}
	resetTokenMu.Unlock()
}

// ---------- Helper ----------

func doRequest(r *gin.Engine, method, path string, body interface{}, headers map[string]string) *httptest.ResponseRecorder {
	var buf bytes.Buffer
	if body != nil {
		_ = json.NewEncoder(&buf).Encode(body)
	}
	req := httptest.NewRequest(method, path, &buf)
	req.Header.Set("Content-Type", "application/json")
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	return w
}

// ---------- User tests ----------

func TestGetUsers_Empty(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/users", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var result []User
	if err := json.NewDecoder(w.Body).Decode(&result); err != nil {
		t.Fatal(err)
	}
	if len(result) != 0 {
		t.Fatalf("expected empty list, got %d items", len(result))
	}
}

func TestCreateUser_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	if w.Code != http.StatusCreated {
		t.Fatalf("expected 201, got %d: %s", w.Code, w.Body.String())
	}
	var u User
	if err := json.NewDecoder(w.Body).Decode(&u); err != nil {
		t.Fatal(err)
	}
	if u.Name != "Alice" || u.Email != "alice@example.com" {
		t.Fatalf("unexpected user: %+v", u)
	}
	if u.Password != "" {
		t.Fatal("password should be hidden in response")
	}
}

func TestCreateUser_MissingFields(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/users", map[string]string{"name": "Bob"}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestCreateUser_ShortPassword(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Bob",
		"email":    "bob@example.com",
		"password": "short",
	}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestGetUserByID_Found(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":  "Alice",
		"email": "alice@example.com",
	}, nil)

	w := doRequest(r, http.MethodGet, "/api/users/1", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var u User
	_ = json.NewDecoder(w.Body).Decode(&u)
	if u.ID != 1 {
		t.Fatalf("expected id=1, got %d", u.ID)
	}
}

func TestGetUserByID_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/users/99", nil, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

func TestGetUserByID_InvalidID(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/users/abc", nil, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestUpdateUser_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":  "Alice",
		"email": "alice@example.com",
	}, nil)

	w := doRequest(r, http.MethodPut, "/api/users/1", map[string]string{
		"name": "Alice Updated",
	}, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", w.Code, w.Body.String())
	}
	var u User
	_ = json.NewDecoder(w.Body).Decode(&u)
	if u.Name != "Alice Updated" {
		t.Fatalf("expected updated name, got %q", u.Name)
	}
}

func TestUpdateUser_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPut, "/api/users/99", map[string]string{"name": "X"}, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

func TestDeleteUser_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":  "Alice",
		"email": "alice@example.com",
	}, nil)

	w := doRequest(r, http.MethodDelete, "/api/users/1", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}

	w2 := doRequest(r, http.MethodGet, "/api/users/1", nil, nil)
	if w2.Code != http.StatusNotFound {
		t.Fatalf("user should be deleted, got %d", w2.Code)
	}
}

func TestDeleteUser_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodDelete, "/api/users/99", nil, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

// ---------- Product tests ----------

func TestGetProducts_Empty(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/products", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var result []Product
	_ = json.NewDecoder(w.Body).Decode(&result)
	if len(result) != 0 {
		t.Fatalf("expected empty list, got %d", len(result))
	}
}

func TestCreateProduct_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/products", map[string]interface{}{
		"name":        "Widget",
		"description": "A fine widget",
		"price":       9.99,
	}, nil)
	if w.Code != http.StatusCreated {
		t.Fatalf("expected 201, got %d: %s", w.Code, w.Body.String())
	}
	var p Product
	_ = json.NewDecoder(w.Body).Decode(&p)
	if p.Name != "Widget" || p.Price != 9.99 {
		t.Fatalf("unexpected product: %+v", p)
	}
}

func TestCreateProduct_MissingFields(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/products", map[string]string{"name": "Widget"}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestGetProductByID_Found(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/products", map[string]interface{}{
		"name":  "Widget",
		"price": 9.99,
	}, nil)

	w := doRequest(r, http.MethodGet, "/api/products/1", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var p Product
	_ = json.NewDecoder(w.Body).Decode(&p)
	if p.ID != 1 {
		t.Fatalf("expected id=1, got %d", p.ID)
	}
}

func TestGetProductByID_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/products/99", nil, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

func TestGetProductByID_InvalidID(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodGet, "/api/products/abc", nil, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestUpdateProduct_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/products", map[string]interface{}{
		"name":  "Widget",
		"price": 9.99,
	}, nil)

	newPrice := 19.99
	w := doRequest(r, http.MethodPut, "/api/products/1", map[string]interface{}{
		"name":  "Widget Pro",
		"price": newPrice,
	}, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", w.Code, w.Body.String())
	}
	var p Product
	_ = json.NewDecoder(w.Body).Decode(&p)
	if p.Name != "Widget Pro" || p.Price != newPrice {
		t.Fatalf("unexpected product after update: %+v", p)
	}
}

func TestUpdateProduct_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	price := 5.0
	w := doRequest(r, http.MethodPut, "/api/products/99", map[string]interface{}{"price": &price}, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

func TestDeleteProduct_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/products", map[string]interface{}{
		"name":  "Widget",
		"price": 9.99,
	}, nil)

	w := doRequest(r, http.MethodDelete, "/api/products/1", nil, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}

	w2 := doRequest(r, http.MethodGet, "/api/products/1", nil, nil)
	if w2.Code != http.StatusNotFound {
		t.Fatalf("product should be deleted, got %d", w2.Code)
	}
}

func TestDeleteProduct_NotFound(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodDelete, "/api/products/99", nil, nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", w.Code)
	}
}

// ---------- Auth tests ----------

func createUserAndLogin(t *testing.T, r *gin.Engine) string {
	t.Helper()
	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	w := doRequest(r, http.MethodPost, "/api/login", map[string]string{
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("login failed: %d %s", w.Code, w.Body.String())
	}
	var resp map[string]interface{}
	_ = json.NewDecoder(w.Body).Decode(&resp)
	token, _ := resp["token"].(string)
	return token
}

func TestLogin_Success(t *testing.T) {
	resetState()
	r := setupRouter()
	token := createUserAndLogin(t, r)
	if token == "" {
		t.Fatal("expected non-empty token")
	}
}

func TestLogin_InvalidPassword(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	w := doRequest(r, http.MethodPost, "/api/login", map[string]string{
		"email":    "alice@example.com",
		"password": "wrongpass",
	}, nil)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401, got %d", w.Code)
	}
}

func TestLogin_UnknownEmail(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/login", map[string]string{
		"email":    "nobody@example.com",
		"password": "secret123",
	}, nil)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401, got %d", w.Code)
	}
}

func TestLogin_MissingFields(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/login", map[string]string{"email": "a@b.com"}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestLogout_Success(t *testing.T) {
	resetState()
	r := setupRouter()
	token := createUserAndLogin(t, r)

	w := doRequest(r, http.MethodPost, "/api/logout", nil, map[string]string{
		"Authorization": token,
	})
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", w.Code, w.Body.String())
	}
}

func TestLogout_MissingToken(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/logout", nil, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestForgotPassword_KnownEmail(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	w := doRequest(r, http.MethodPost, "/api/forgot-password", map[string]string{
		"email": "alice@example.com",
	}, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var resp map[string]interface{}
	_ = json.NewDecoder(w.Body).Decode(&resp)
	if _, ok := resp["reset_token"]; !ok {
		t.Fatal("expected reset_token in response")
	}
}

func TestForgotPassword_UnknownEmail(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/forgot-password", map[string]string{
		"email": "nobody@example.com",
	}, nil)
	// Should still return 200 to avoid user enumeration
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var resp map[string]interface{}
	_ = json.NewDecoder(w.Body).Decode(&resp)
	if _, ok := resp["reset_token"]; ok {
		t.Fatal("reset_token should NOT be present for unknown email")
	}
}

func TestResetPassword_Success(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	fw := doRequest(r, http.MethodPost, "/api/forgot-password", map[string]string{
		"email": "alice@example.com",
	}, nil)
	var fr map[string]interface{}
	_ = json.NewDecoder(fw.Body).Decode(&fr)
	resetToken := fr["reset_token"].(string)

	w := doRequest(r, http.MethodPost, "/api/reset-password", map[string]string{
		"token":    resetToken,
		"password": "newpassword",
	}, nil)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", w.Code, w.Body.String())
	}

	// Verify new password works
	lw := doRequest(r, http.MethodPost, "/api/login", map[string]string{
		"email":    "alice@example.com",
		"password": "newpassword",
	}, nil)
	if lw.Code != http.StatusOK {
		t.Fatalf("login with new password failed: %d %s", lw.Code, lw.Body.String())
	}
}

func TestResetPassword_InvalidToken(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/reset-password", map[string]string{
		"token":    "invalidtoken",
		"password": "newpassword",
	}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestResetPassword_ShortPassword(t *testing.T) {
	resetState()
	r := setupRouter()

	w := doRequest(r, http.MethodPost, "/api/reset-password", map[string]string{
		"token":    "anytoken",
		"password": "short",
	}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", w.Code)
	}
}

func TestResetPassword_ExpiredToken(t *testing.T) {
	resetState()
	r := setupRouter()

	doRequest(r, http.MethodPost, "/api/users", map[string]string{
		"name":     "Alice",
		"email":    "alice@example.com",
		"password": "secret123",
	}, nil)

	// Manually insert an expired reset token
	expiredToken := "expiredtoken123"
	resetTokenMu.Lock()
	resetTokens[expiredToken] = resetToken{userID: 1, expiresAt: time.Now().Add(-1 * time.Hour)}
	resetTokenMu.Unlock()

	w := doRequest(r, http.MethodPost, "/api/reset-password", map[string]string{
		"token":    expiredToken,
		"password": "newpassword",
	}, nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("expected 400 for expired token, got %d", w.Code)
	}
}

func TestGenerateToken(t *testing.T) {
	t1, err := generateToken()
	if err != nil {
		t.Fatal(err)
	}
	t2, err := generateToken()
	if err != nil {
		t.Fatal(err)
	}
	if t1 == "" || t2 == "" {
		t.Fatal("tokens should not be empty")
	}
	if t1 == t2 {
		t.Fatal("tokens should be unique")
	}
	if len(t1) != 32 { // 16 bytes hex-encoded = 32 chars
		t.Fatalf("unexpected token length: %d", len(t1))
	}
}
