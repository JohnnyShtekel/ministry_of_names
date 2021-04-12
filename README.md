# ministry of names service

A large government of a country with 1,000,000,000 citizens would like to keep a directory of their first names. This country demands that each citizen have a unique name. So, when parents want to register a new baby name, they must go to the ministry of names, and come up with a unique name for their new born.


ministry of names service expose two end points :
* register a new citizen by first name. 
*  filter by first_name prefix.


### architecture design
![](http://mindmappingsoftwareblog.com/wp-content/uploads/2017/03/large-whiteboard.jpg)

elasticsearch was chosen as the main database beacuse the fast searches, and redis for cache.
The goal is basically to register users by their first name but avoid a similar name (distance of one edit). Plus you will have the ability to search for registered users quickly.

**Registration**: Elasticsearch provides the ability to make fuzznies-based queries. And in fact before registration prevent registration of similar names (one edit distance). The edge case is the one that takes a elasticsearch after inserting an index time (if you want to query with fuzzines). So if there are more the one users who register almost at the same time with a similar name both will be able to register, which is a bad situation. To solve the problem I used and expanded the hamming
 circle alogiritm and basically I got every request to register the name and out of the algorithms I would get all the permutations of the similar names. (johnny -> johnn -> gohnny) Create a list of all strings within hamming distance of a reference string with a given alphabet and checks by the ID if it exists in elasticsearch. And in order to save inquiries to elasticsearch every time a user is saved I would save all the permutations of his name in redis as a cache mechanism and save inquiries to elasticsearch in the future.
 
 **Searching**:  elasticsearch is a well-known tool that can be used to perform complex searches quickly. In this case the search is performed by the private id which is the unique id by prefix.
I was wondering if to put the redis as a cache mechanism for searches as well but since elastic in any case contains an excellent cache mechanism then there was no need. In addition it was not defined that user deletions should be done in the meantime so I did not have to go into the implementation of invalidation.


![](https://i.imgur.com/e0scCh8.png)


### Prerequisites
Make sure you have installed all of the following prerequisites on your development machine:
1. git
2. docke

## Service Deployment

```bash
git clone git remote add origin https://github.com/JohnnyShtekel/ministry_of_names.git
cd {project_path}
docker-compose up
```

## How it works
basic flow:

**register new citizen by first name as unique id and by last name:**
```bash
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ \ 
   "first_name": "John", \ 
   "last_name": "Wick" \ 
 }' 'http://0.0.0.0:5000/api/v1/ministry_of_names/citizen'
```

**search for registerd citizens by prefix of the first name:**

```bash
curl -X GET --header 'Accept: application/json' 'http://0.0.0.0:5000/api/v1/ministry_of_names/citizen?first_name=jo'
```
## Swagger-ui
to reveal the API docs there's a need to use a swagger-ui
http://0.0.0.0:5000/api/v1/ministry_of_names/ui/

## Stack

* **Flask**
* **Redis DB** 
* **Pytest**
* **Elasticsearch**
* **Swagger**






## License
[MIT](https://choosealicense.com/licenses/mit/)