http -v POST localhost:5000/sign-up name=송은우 email=songew@gmail.com
password=test1234
POST /sign-up HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 83
Content-Type: application/json 
Host: localhost: 5000
User-Agent: HTTPie/0.9.9
{
"email": "songew@gmail.com", "name": "$°9",
"password": "test1234",
"profile": "Christian. Software Engineer. Serial Entrepreneur. BookAuthor"
}
НТТP/1.0 200 OK