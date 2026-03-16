const cars = [];
let nextId = 1;

function validateRequiredString(value, fieldName) {
	if (typeof value !== "string" || value.trim().length === 0) {
		throw new Error(`${fieldName} is required.`);
	}
}

function validateMake(make) {
	validateRequiredString(make, "Make");
}

function validateModel(model) {
	validateRequiredString(model, "Model");
}

function validateYear(year) {
	const currentYear = new Date().getFullYear();
	if (
		typeof year !== "number" ||
		!Number.isInteger(year) ||
		year < 1886 ||
		year > currentYear + 1
	) {
		throw new Error(
			`Year must be an integer between 1886 and ${currentYear + 1}.`
		);
	}
}

function validateColor(color) {
	if (typeof color !== "string" || color.trim().length === 0) {
		throw new Error("Color must be a non-empty string.");
	}
}

function validatePrice(price) {
	if (typeof price !== "number" || !isFinite(price) || price < 0) {
		throw new Error("Price must be a non-negative number.");
	}
}

function getCars() {
	return [...cars];
}

function getCarById(id) {
	return cars.find((car) => car.id === id) || null;
}

function addCar(payload) {
	const { make, model, year, color, price } = payload || {};

	validateMake(make);
	validateModel(model);
	validateYear(year);

	if (color !== undefined) {
		validateColor(color);
	}

	if (price !== undefined) {
		validatePrice(price);
	}

	const car = {
		id: nextId,
		make: make.trim(),
		model: model.trim(),
		year,
		...(color !== undefined && { color: color.trim() }),
		...(price !== undefined && { price }),
		createdAt: new Date().toISOString(),
	};

	nextId += 1;
	cars.push(car);

	return car;
}

function updateCar(id, payload) {
	const car = cars.find((item) => item.id === id);

	if (!car) {
		throw new Error("Car not found.");
	}

	const { make, model, year, color, price } = payload || {};

	if (make !== undefined) {
		validateMake(make);
		car.make = make.trim();
	}

	if (model !== undefined) {
		validateModel(model);
		car.model = model.trim();
	}

	if (year !== undefined) {
		validateYear(year);
		car.year = year;
	}

	if (color !== undefined) {
		if (color === null) {
			delete car.color;
		} else {
			validateColor(color);
			car.color = color.trim();
		}
	}

	if (price !== undefined) {
		if (price === null) {
			delete car.price;
		} else {
			validatePrice(price);
			car.price = price;
		}
	}

	car.updatedAt = new Date().toISOString();

	return car;
}

function deleteCar(id) {
	const index = cars.findIndex((car) => car.id === id);

	if (index === -1) {
		throw new Error("Car not found.");
	}

	const [deletedCar] = cars.splice(index, 1);
	return deletedCar;
}

module.exports = {
	getCars,
	getCarById,
	addCar,
	updateCar,
	deleteCar,
};
