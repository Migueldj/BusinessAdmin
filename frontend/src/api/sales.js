import axios from "axios"

export const testEP = (data) => {
    return axios.post("http://localhost:8000/api/test/", data)
}