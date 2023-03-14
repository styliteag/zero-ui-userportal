import axios from 'axios'


let axiosBaseURL = location.protocol + "//" + location.hostname + ":" + location.port + "/api/";


//Create a axios instance, And set timeout to 30s
const zeroapi = axios.create({
    baseURL: axiosBaseURL,
    timeout: 30000,
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: false,
});



export { zeroapi }