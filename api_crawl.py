import requests

# base_url = 'https://api-dev.nsls2.bnl.gov/v1/'
base_url = 'https://api.nsls2.bnl.gov/v1/'
# endpoint = 'https://api-dev.nsls2.bnl.gov/v1/facility/nsls2/cycles'
r = requests.get(base_url + 'facility/nsls2/cycles/')
cycles = r.json()['cycles']
proposal_count = 0

for cycle in cycles:
    print(cycle)
    # r = requests.get(base_url + 'proposals/?cycle=' + cycle + '&facility=nsls2&page_size=10&page=1&include_directories=false')
    # r = requests.get(base_url + 'proposals/?cycle=' + cycle + '&facility=nsls2&page_size=0&include_directories=false')
    route = 'facility/nsls2/cycle/' + cycle + '/proposals'
    r = requests.get(base_url + route)
    if r.status_code == 200:
        proposals = r.json()['proposals']    
        for proposal_id in proposals:
            proposal_count += 1
            print(proposal_id)
            r = requests.get(base_url + 'proposal/' + proposal_id)
            if r.status_code != 200:
                print(r.json())
    else:
        print(cycle + ' status code: ' + r.status_code)

print(proposal_count)