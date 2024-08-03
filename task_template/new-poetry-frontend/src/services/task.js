import axios from 'axios'

const baseUrl = "/api/v1/task"

const submitUserInput = (newUserMessage) => {
  const request = axios.post(`${baseUrl}/process`, newUserMessage)
  return request.then(response => response.data)
}

const finishTask = (rating) => {
  console.log(`finish ${rating}`)
}

export default { 
  submitUserInput, 
  finishTask
}