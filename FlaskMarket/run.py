from market import app
from market.models import Item, User

if __name__=="__main__":
    with app.app_context():
        items=Item.query.all()
        users=User.query.all()
    app.run(debug=True)