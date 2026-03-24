const express = require("express");
const bcrypt = require("bcryptjs");
const path = require("path");
const { requireGuest, requireAuth } = require("../middleware/auth");

const router = express.Router();

// In-memory user store (replace with a database in production)
const users = [];

// GET / → redirect based on session
router.get("/", (req, res) => {
	if (req.session.userId) {
		return res.redirect("/dashboard");
	}
	res.redirect("/login");
});

// GET /login
router.get("/login", requireGuest, (req, res) => {
	res.sendFile(path.join(__dirname, "../views/login.html"));
});

// POST /login
router.post("/login", requireGuest, async (req, res) => {
	const { email, password } = req.body;

	if (!email || !password) {
		return res.status(400).json({ error: "Email and password are required." });
	}

	const user = users.find((u) => u.email.toLowerCase() === email.toLowerCase());

	if (!user) {
		return res.status(401).json({ error: "Invalid email or password." });
	}

	const passwordMatch = await bcrypt.compare(password, user.passwordHash);

	if (!passwordMatch) {
		return res.status(401).json({ error: "Invalid email or password." });
	}

	req.session.userId = user.id;
	req.session.userName = user.name;

	res.json({ message: "Login successful.", redirect: "/dashboard" });
});

// GET /register
router.get("/register", requireGuest, (req, res) => {
	res.sendFile(path.join(__dirname, "../views/register.html"));
});

// POST /register
router.post("/register", requireGuest, async (req, res) => {
	const { name, email, password } = req.body;

	if (!name || !email || !password) {
		return res.status(400).json({ error: "Name, email and password are required." });
	}

	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	if (!emailRegex.test(email)) {
		return res.status(400).json({ error: "Invalid email format." });
	}

	if (password.length < 6) {
		return res.status(400).json({ error: "Password must be at least 6 characters." });
	}

	const duplicate = users.some((u) => u.email.toLowerCase() === email.toLowerCase());
	if (duplicate) {
		return res.status(409).json({ error: "Email already registered." });
	}

	const passwordHash = await bcrypt.hash(password, 10);
	const user = {
		id: users.length + 1,
		name: name.trim(),
		email: email.trim().toLowerCase(),
		passwordHash,
		createdAt: new Date().toISOString(),
	};

	users.push(user);

	req.session.userId = user.id;
	req.session.userName = user.name;

	res.status(201).json({ message: "Account created.", redirect: "/dashboard" });
});

// GET /api/me (protected)
router.get("/api/me", requireAuth, (req, res) => {
	res.json({ id: req.session.userId, name: req.session.userName });
});

// GET /dashboard (protected)
router.get("/dashboard", requireAuth, (req, res) => {
	res.sendFile(path.join(__dirname, "../views/dashboard.html"));
});

// POST /logout
router.post("/logout", requireAuth, (req, res) => {
	req.session.destroy(() => {
		res.json({ message: "Logged out.", redirect: "/login" });
	});
});

module.exports = router;
