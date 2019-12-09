const get = (url, body) => {
    preloader.style.display = 'block';
    load.style.display = 'none';
    return fetch(url, {body: body, method: 'POST', headers: {'Content-Type': 'application/json'}})
        .then(resp => {
            if (!resp.ok) {
                throw Error;
            }
            return resp
        })
        .then(resp => {
            return resp.json();
        })
        .then(data => {
            preloader.style.display = 'none';
            load.style.display = 'block';
            load.setAttribute('href', data['filename']);
        })
        .catch(error => {
            console.log(`some error occurred: ${error}`)
        });
};

const button = document.querySelector('.index__form-btn');
const preloader = document.querySelector('#index__result-preloader');
const load = document.querySelector("#index__result-load");
const input = document.querySelector('#index__form-amount');

const parseInvoke = () => {
    const baseUrl = 'parse';
    button.addEventListener('click', () => {
        let amount = parseInt(input.value);
        get(baseUrl, JSON.stringify({amount: amount}));
    })
};

parseInvoke();