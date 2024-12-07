import uvicorn
from serwer.server import BedServer

bed_server = BedServer()
app = bed_server.app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
