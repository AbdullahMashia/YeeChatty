// REST Countries API Example
const response = await fetch('https://restcountries.com', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
});

const data = await response.json();
console.log(data);