import './Error.css';
import React from 'react'

class ErrorDoc extends React.Component {

	parseJSONtoTable() {
		let tableHTML = "";
		let i = 0;
		let tableData = JSON.parse('"code": 123,"errorName": "test","description": "testDesc","errorMessage": "testErrorMsg"');
		//let tableData = JSON.parse('"code": 123,"errorName": "test","description": "testDesc","errorMessage": "testErrorMsg","code": 123,"errorName": "test",description": "testDesc","errorMessage": "testErrorMsg"]");

	    tableHTML += "<table>";
	    for (i in tableData) 
	    	tableHTML += "<tr><td>" + tableData[i] + "</td></tr>";
	    
	    tableHTML += "</table>";

	    return tableHTML;
	}

    render() {
        return (
        	<div>
	            <table class="tableizer-table">
    				<thead><tr class="tableizer-firstrow"><th>Code</th><th>Name</th><th>Description</th><th>Error Message</th></tr>
    				</thead>
    				<tbody>
						<tr><td>0</td><td>SUCCESS</td><td>Returned: %d, no error has occurred</td><td>NULL</td></tr>
						<tr><td>1</td><td>UNKNOWN_ERROR</td><td>Returned: %d, an unknown error has occurred %s</td><td>An Unexpected Error has occured</td></tr>
						<tr><td>2</td><td>INVALID_INPUT</td><td>the input given doesnt work</td><td>invalid input expected expected_format</td></tr>
						<tr><td>3</td><td>FILE_NOT_FOUND</td><td>Returned: %d, file %s was not found</td><td>&nbsp;</td></tr>
						<tr><td>4</td><td>CANT_CREATE_FILE</td><td>Returned: %d, file %s could not be created</td><td>&nbsp;</td></tr>
						<tr><td>5</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>6</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>7</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>8</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>9</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>10</td><td>INVLAID_REQUEST</td><td>Returned %d, invalid request %s</td><td>&nbsp;</td></tr>
						<tr><td>11</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>12</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>13</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>14</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>15</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>16</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>17</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>18</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>19</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>20</td><td>ATTRIBUTE_NOT_FOUND</td><td>Returned: %d, Attribute %s could not be found.</td><td>&nbsp;</td></tr>
						<tr><td>21</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>22</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>23</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>24</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>25</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>26</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>27</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>28</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>29</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>30</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>31</td><td>AUTHENICATION_ERROR</td><td>failed to login</td><td>Login attempt fail please check username and password</td></tr>
						<tr><td>32</td><td>INVALID_USERNAME</td><td>Given username is invalid to use</td><td>&nbsp;</td></tr>
						<tr><td>33</td><td>NOT_LOGGED_IN</td><td>Returned %d: not logged in</td><td>&nbsp;</td></tr>
						<tr><td>34</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>35</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>36</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>37</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>38</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>39</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>40</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>41</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>42</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>43</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>44</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>45</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>46</td><td>CONNECTION_FAILED</td><td>connection could not be made to server</td><td>Connection to user_name@computer_name could not be made</td></tr>
						<tr><td>47</td><td>CONNECTION_DROPPED</td><td>the connection ending when the script was running</td><td>Connection to computer_name was lost</td></tr>
						<tr><td>48</td><td>Error in scipt</td><td>The script exited with a non 0 code</td><td>The Script failed with error code error Code</td></tr>
						<tr><td>49</td><td>CANT_FIND_SSH_KEY</td><td>couldnt find the ssh key in PRIVATE_SSH_KEY_PATH</td><td>Returned %d: failed to find a valid ssh key at %s</td></tr>
						<tr><td>50</td><td>SSH_AUTHENTICATION_FAILED</td><td>ssh connection couldnt be made due to autentication</td><td>Returned %d: failed authentication over ssh for user_name@computer_name </td></tr>
						<tr><td>51</td><td>EMPTY_SSH_PUBLIC_KEY</td><td>SSH public key entry is empty in the config</td><td>Returned %d: PUBLIC_SSH_KEY_VALUE config is empty</td></tr>
						<tr><td>52</td><td>SSH_PERMISSION_DENIED</td><td>Couldnt access folder</td><td>"Returned %d: permission denied accessing: %s"</td></tr>
						<tr><td>53</td><td>SSH_FAILED_TO_EXECUTE_SCRIPT</td><td>Failed to execute the script (failed to connect/ lost connection)</td><td>"Returned %d: failed to execute script: %s"</td></tr>
						<tr><td>54</td><td>SSH_SCRIPT_FAILED_WITH_ERROR_CODE</td><td>script ended with a non-zero error code</td><td>"Returned:%d, script failed with error code: %s"</td></tr>
						<tr><td>55</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>56</td><td>ERROR_BLACKLISTED_COMMAND</td><td>Script contains blacklisted command</td><td>"Returned%d, script contained invalid command: %s"</td></tr>
						<tr><td>57</td><td>EOR_BLACKLISTED_IP</td><td>Connection IP is blacklisted</td><td>"returned: %d, ip %s is blacklisted"</td></tr>
						<tr><td>58</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>59</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>60</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>61</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>62</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>63</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>64</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>65</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>66</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>67</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>68</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>69</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>70</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>71</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>72</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>73</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>74</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>75</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>76</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>77</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>78</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>79</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>80</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>81</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>82</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>83</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>84</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr><td>85</td><td>&nbsp;</td><td>&nbsp;</td><td></td></tr>
					</tbody>
				</table>
			</div>
        );
	}
}

export default ErrorDoc
