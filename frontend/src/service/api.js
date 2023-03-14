import axios from 'axios'

const env = process.env.NODE_ENV || "production";


let axiosBaseURL = location.protocol + "//" + location.hostname + ":" + location.port;


//Create a axios instance, And set timeout to 30s
const api = axios.create({
    baseURL: axiosBaseURL,
    timeout: 30000,
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: false,
});



export { api }