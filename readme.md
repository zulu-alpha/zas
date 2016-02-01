# Installation
Copy the config and logs folders to ```/c/Users/adam/zas/config/``` 
(or something like ```C:\Users\adam\zas\config``` in Windows if using Babun)
This funny path is there to improve dev prod similarity and be able to use the same 
compose file to start the stack (Canonical compose file).

Edit them with the appropriate settings (such as secrets).

Use ```docker-compose run```