import python.main
from uvicorn import main as uvicorn_main
if __name__=="__main__":
    uvicorn_main(["main:app","--reload"])