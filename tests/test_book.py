import pytest

def test_get_book(client):

    res = client.post("/graphql/book_ep", json={
        "query": """
        {
            allbooks{
                id authorId
            }
        }
        """
    })


    assert res.status_code == 200

@pytest.mark.parametrize("id, response", [
    (
        1, 1
    ),
    (
        2, None
    ),
    (
        3, 3
    ),
])
def test_get_book_by_id(client, id, response):
    res = client.post("/graphql/book_ep", json={
        "query": """
        {
            bookById(id: %s){
                id authorId
            }
        }
        """ % (id)
    })

    data =  res.json

    # data['bookById'][id] == response
    # print (type(data['bookById']))
    # re
    # assert res. == 200
    # assert res.status_code == 200
# def test_get_book(test_client):

#     res = test_client.post("/graphql/book_ep")



# def test_get_book(test_client):

#     res = test_client.post("/graphql/book_ep")

#     assert res.status_code == 200
