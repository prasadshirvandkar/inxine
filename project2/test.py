# Assignment 1 -> Project 1 - Phase 1
import pickle

if __name__ == "__main__":
    project2_index_details = {
        "ip": "3.22.51.186",
        "port": "9999",
        "name": "execute_query",
        "env": "prod"
    }

    #with open('data/project2_index_details.pickle', 'wb') as handle:
        #pickle.dump(project2_index_details, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('data/project2_index_details.pickle', 'rb') as handle:
        unserialized_data = pickle.load(handle)

    print(f"IP: {unserialized_data['ip']}")
    print(f"Port: {unserialized_data['port']}")
    print(f"Name: {unserialized_data['name']}")
    print(f"Env: {unserialized_data['env']}")
