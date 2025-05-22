import yaml
from fastapi import FastAPI

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config("./conf.yaml")
print(config)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello"}



def main():
    host = config["system_config"]["host"]
    port = config["system_config"]["port"]
    print(f"Starting server on {host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
