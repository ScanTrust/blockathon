# smart-label-vuejs

> A Vue.js project

To run this as a demo, specify the correct endpoints in src/config.js

```
st_config: {
  'API_BASE_URL': 'http://localhost:5000/api/v2/consumer/' # Mocked API included in the backend project
},
ts_config: {
  'API_BASE_URL': 'https://sometradeshift.url/'
},
bdb_config: {
  'API_BASE_URL': 'http://51.144.103.72:9984/api/v1/', # BigChainDb endpoint included in docker compose
  'TOKEN_ID': 'f94e7a2af781da96ea398c23cf676d0403ca90f233a336d31ed5d2a67414d084' # Minted token on bigchainDB
},
euipo_config: {
  'EUIPO_URL': 'http://services.blockathon.eu/'
},
st_proxy_config: {
  'API_BASE_URL': 'http://localhost:5000/api/' # BigChain API included in the backend project
}
}
```

These URLs can be used to get an example result from a code redirection.

Genuine

{frontend_url}/#/consumer-impact?uid=uuid-mock-genuine&api_key=eyJjYW1wYWlnbl9pZCI6NTg3fQ%3A1fWjmQ%3AxIRYGZMwxh4f88uau1pf5uk50CE&qr=15F9341F5606106E34D39ABC&install_id=123

{frontend_url}/#/consumer-impact?uid=uuid-mock-blacklisted&api_key=eyJjYW1wYWlnbl9pZCI6NTg3fQ%3A1fWjmQ%3AxIRYGZMwxh4f88uau1pf5uk50CE&qr=15F9341F5606106E34D39ABC&install_id=123

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
