/**
 * Calculates the square of a number (n²).
 * A perfect square is the result of multiplying an integer by itself,
 * but this function accepts any finite number.
 * @param {number} n - The number to square.
 * @returns {number} The square of n.
 */
function perfectSquare(n) {
	if (typeof n !== "number" || !Number.isFinite(n)) {
		throw new Error("Input must be a finite number.");
	}
	return n * n;
}

module.exports = { perfectSquare };
