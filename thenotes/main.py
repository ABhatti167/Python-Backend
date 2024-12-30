# the reason we can do this is because website is a package
# as it has init and stuff from init can easliy be imported
from website import create_app 

app = create_app()

if __name__ == "__main__": 
    app.run(debug=True)
     