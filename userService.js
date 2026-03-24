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

function getUsers() {
	return [...users];
}

function getUserById(id) {
	return users.find((user) => user.id === id) || null;
}

function addUser(payload) {
	const { name, email } = payload || {};

	validateName(name);
	validateEmail(email);

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
		createdAt: new Date().toISOString(),
	};

	nextId += 1;
	users.push(user);

	return user;
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

module.exports = {
	getUsers,
	getUserById,
	addUser,
	updateUser,
	deleteUser,
};
