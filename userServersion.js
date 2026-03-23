const users = [];
let nextId = 1;

function validateName(name) {
	if (typeof name !== "string" || name.trim().length === 0) {
		throw new Error("Name is required.");
	}
}

function validateEmail(email) {
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

	if (typeof email !== "string" || !emailRegex.test(email)) {
		throw new Error("Email is invalid.");
	}
}

function validatePassword(password) {
	if (typeof password !== "string" || password.length < 6) {
		throw new Error("Password must be at least 6 characters.");
	}
}

function getUsers() {
	return [...users];
}

function getUserById(id) {
	return users.find((user) => user.id === id) || null;
}

function addUser(payload) {
	const { name, email, password } = payload || {};

	validateName(name);
	validateEmail(email);
	validatePassword(password);

	const duplicated = users.some(
		(user) => user.email.toLowerCase() === email.toLowerCase()
	);

	if (duplicated) {
		throw new Error("Email already exists.");
	}

	const user = {
		id: nextId,
		name: name.trim(),
		email: email.trim(),
		password,
		createdAt: new Date().toISOString(),
	};

	nextId += 1;
	users.push(user);

	return { id: user.id, name: user.name, email: user.email, createdAt: user.createdAt };
}

function updateUser(id, payload) {
	const user = users.find((item) => item.id === id);

	if (!user) {
		throw new Error("User not found.");
	}

	const { name, email } = payload || {};

	if (name !== undefined) {
		validateName(name);
		user.name = name.trim();
	}

	if (email !== undefined) {
		validateEmail(email);

		const duplicated = users.some(
			(item) => item.id !== id && item.email.toLowerCase() === email.toLowerCase()
		);

		if (duplicated) {
			throw new Error("Email already exists.");
		}

		user.email = email.trim();
	}

	user.updatedAt = new Date().toISOString();

	return user;
}

function deleteUser(id) {
	const index = users.findIndex((user) => user.id === id);

	if (index === -1) {
		throw new Error("User not found.");
	}

	const [deletedUser] = users.splice(index, 1);
	return deletedUser;
}

function authenticateUser(email, password) {
	if (typeof email !== "string" || typeof password !== "string") {
		throw new Error("Email and password are required.");
	}

	const user = users.find(
		(u) => u.email.toLowerCase() === email.toLowerCase()
	);

	if (!user || user.password !== password) {
		throw new Error("Invalid email or password.");
	}

	return { id: user.id, name: user.name, email: user.email };
}

module.exports = {
	getUsers,
	getUserById,
	addUser,
	updateUser,
	deleteUser,
	authenticateUser,
};
