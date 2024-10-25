from fastapi import HTTPException, status


noauth = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
noapi = HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                      detail = "This Rquest Only For HTML View")
notfound = HTTPException(status_code = status.HTTP_404_NOT_FOUND)
