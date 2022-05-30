import axios from "axios"

export const createSale = (data) => {
    return axios.post("http://localhost:8000/api/create-sale/", data)
}