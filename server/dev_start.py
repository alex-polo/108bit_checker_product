import uvicorn

if __name__ == '__main__':
    uvicorn.run("src.main:app",
                host="0.0.0.0",
                port=8443,
                workers=1,
                log_level="info",
                reload=True
                )