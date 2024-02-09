import requests

base_url = 'https://api-dev.nsls2.bnl.gov/v1/'
# endpoint = 'https://api-dev.nsls2.bnl.gov/v1/facility/nsls2/cycles'
r = requests.get(base_url + 'facility/nsls2/cycles/')
cycles = r.json()['cycles']

for cycle in cycles:
    print(cycle)
    r = requests.get(base_url + 'proposals/?cycle=' + cycle + '&facility=nsls2&page_size=10&page=1&include_directories=false')
    proposals = r.json()['proposals']    
    for proposal in proposals:
        proposal_id = proposal['proposal_id']
        print(proposal_id)
        r = requests.get(base_url + 'proposal/' + proposal_id)
        print(r.json())