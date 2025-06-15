from app import create_app
import uvicorn


if __name__ == '__main__':
    uvicorn.run("app:create_app", host="127.0.0.1", port=5000, factory=True ,reload=True)
