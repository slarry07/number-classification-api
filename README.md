# Number Classification API

This API classifies a given number and returns its mathematical properties along with a fun fact.

## Usage

### Endpoint
`GET /api/classify-number?number=<number>`

### Example Request
`GET /api/classify-number?number=371`

### Example Response
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 2^3 = 371"
}
