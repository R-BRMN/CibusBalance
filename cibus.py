#!/usr/bin/python

import requests
import fire

CIBUS_URL = 'https://www.mysodexo.co.il'

def _get_viewstate():
	'''Returns a VIEWSTATE string used to interact with the Cibus site'''

	res = requests.get(CIBUS_URL)
	viewstate = res.text.split('VIEWSTATE')[2].split('"')[2]
	return viewstate

def _get_login_payload(username, password, organization, viewstate):
	'''Returns a payload used to login to the Cibus site'''

	payload = {
		'__VIEWSTATE': viewstate,
		'txtUsr': f'{username}|{organization}',
		'hidUsr': username,
		'txtPas': password,
		'txtCmp': organization,
		'ctl12': '',
	}
	return payload

def get_budget(username, password, organization):
	'''Returns the remaining balance in Shekels of a Cibus organizational account'''

	budget_url = f'{CIBUS_URL}/new_ajax_service.aspx?getBdgt=1'
	requests_session = requests.Session()
	payload = _get_login_payload(
		username=username,
		password=password,
		organization=organization,
		viewstate=_get_viewstate()
	)
	requests_session.post(CIBUS_URL, data=payload)
	return requests_session.get(budget_url).text

if __name__ == '__main__':
	fire.Fire(get_budget)
