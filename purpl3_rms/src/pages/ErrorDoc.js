import './Error.css';
import React from 'react'

class ErrorDoc extends React.Component {

	// parseJSONtoTable() 
	// 	let tableHTML = "";
	// 	let i = 0;
	// 	let tableData = JSON.parse('"code": 123,"errorName": "test","description": "testDesc","errorMessage": "testErrorMsg"');
	// 	//let tableData = JSON.parse('"code": 123,"errorName": "test","description": "testDesc","errorMessage": "testErrorMsg","code": 123,"errorName": "test",description": "testDesc","errorMessage": "testErrorMsg"]");

	//     tableHTML += "<table>";
	//     for (i in tableData) 
	//     	tableHTML += "<tr><td>" + tableData[i] + "</td></tr>";
	    
	//     tableHTML += "</table>";

	//     return tableHTML;
	// 

    render() {
        return (
        	<div>
    			<table>
					<thead>
						<tr class="tableizer-firstrow"><th>Code</th><th>Name</th><th>Description</th><th>Error Message</th></tr>
					</thead>
					<tbody>
						<tr>
							<th>0</th>
							<th>SUCCESS</th>
							<th>No Error. Everything works as expected</th>
							<th>Returned: 0, no error has occurred.</th>
						</tr>
						<tr>
							<td>1</td>
							<td>UNKNOWN_ERROR</td>
							<td>An error that hasnt been registar has occurred read error message to see what went wrong.</td>
							<td>Returned: 1, an unknown error has occurred ERROR_MSG.</td>
						</tr>
						<tr>
							<td>2</td>
							<td>INVALID_INPUT</td>
							<td>The given input is incorrect and should be correct for request to go though</td>
							<td>Returned: 2, invalid input.</td>
						</tr>
						<tr>
							<td>3</td>
							<td>FILE_NOT_FOUND</td>
							<td>Couldn't find a file in a given path, this can be due to incorrect path or maybe file doesn't exist</td>
							<td>Returned: 3, file FILE_NAME was not found</td>
						</tr>
						<tr>
							<td>4</td>
							<td>CANT_CREATE_FILE</td>
							<td>Can't create a file. This could be due to a path of a folder that doesn't exist, or the user the server is running under doesn't have permission to the location</td>
							<td>Returned: 4, file FILE_NAME could not be created</td>
						</tr>
						<tr>
							<td>10</td>
							<td>INVALID_REQUEST</td>
							<td>An invalid request was made to the API, This has to do with how to server is set up if this occurs please reach out to the devlopers for assistance</td>
							<td>Returned: 10, invalid request REQUEST</td>
						</tr>
						<tr>
							<td>20</td>
							<td>ATTRIBUTE_NOT_FOUND</td>
							<td>The Attributes given could not be found If this  occurs please reach out to the devlopers for assistance</td>
							<td>Returned: 20, Attribute ATTR_NAME could not be found.</td>
						</tr>
						<tr>
							<td></td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td>31</td>
							<td>AUTHENICATION_ERROR</td>
							<td>Failed to login to the given account please check your username and password</td>
							<td>Returned: 31, failed login for USERNAME</td>
						</tr>
						<tr>
							<td>32</td>
							<td>INVALID_USERNAME</td>
							<td>The given username is not valid please select a new one. username can not include spaces or semi-colons ";"</td>
							<td>Return: 32, failed login due too invalid username</td>
						</tr>
						<tr>
							<td>33</td>
							<td>NOT_LOGGED_IN</td>
							<td>Requests can not be made unless you are logged into an account please login because sending any request to the api</td>
							<td>Returned 33: Not Logged In to user</td>
						</tr>
						<tr>
							<td></td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td>46</td>
							<td>CONNECTION_FAILED</td>
							<td>Connection could not be made to the computer this ussally occures if sshd is not running or if the computer is offline.</td>
							<td>Returned: 46, Connection to user_name@computer_name could not be made</td>
						</tr>
						<tr>
							<td>49</td>
							<td>CANT_FIND_SSH_KEY</td>
							<td>Couldn't find the ssh key in PRIVATE_SSH_KEY_PATH This key should be created with rsa encryption using ssh-keygen</td>
							<td>Returned 49: failed to find a valid ssh key at PATH_TOO_SSH_KEY</td>
						</tr>
						<tr>
							<td>50</td>
							<td>SSH_AUTHENTICATION_FAILED</td>
							<td>SSH connection couldn't be made due to autentication check your username and password and try again.</td>
							<td>Returned 50: failed authentication over ssh for user_name@computer_name </td>
						</tr>
						<tr>
							<td>51</td>
							<td>EMPTY_SSH_PUBLIC_KEY</td>
							<td>SSH public key entry is empty in the config This should be the public key pair of your RSA ssh key</td>
							<td>Returned 51: PUBLIC_SSH_KEY_VALUE config is empty</td>
						</tr>
						<tr>
							<td>52</td>
							<td>SSH_PERMISSION_DENIED</td>
							<td>Couldnt access folder due to permission deined please select a different folder in config or change permissions to the folder. This may happen if the computer shuts off during launching of the script</td>
							<td>Returned 52: permission denied accessing: FILE_NAME</td>
						</tr>
						<tr>
							<td>53</td>
							<td>SSH_FAILED_TO_EXECUTE_SCRIPT</td>
							<td>Failed to execute the script (failed to connect/ lost connection)</td>
							<td>Returned 53: failed to execute script: SCRIPT_NAME</td>
						</tr>
						<tr>
							<td>54</td>
							<td>SSH_SCRIPT_FAILED_WITH_ERROR_CODE</td>
							<td>script ended with a non-zero error code</td>
							<td>Returned:54, script failed with error code: ERROR_CODE</td>
						</tr>
						<tr>
							<td>55</td>
							<td>ERROR_SSH_CONNECTION_LOST</td>
							<td>Lost connection to the ssh client without handshake</td>
							<td>Returned 55: Connection to remote computer USERNAME@IP running script SCRIPT_NAME lost</td>
						</tr>
						<tr>
							<td>56</td>
							<td>ERROR_BLACKLISTED_COMMAND</td>
							<td>Script contains blacklisted command. Ask you administator about what cmd can and cannot be used</td>
							<td>Returned 56, script contained invalid command: BLOCKED_COMMAND</td>
						</tr>
						<tr>
							<td>57</td>
							<td>ERROR_BLACKLISTED_IP</td>
							<td>Connection IP is blacklisted. Ask your administator about this</td>
							<td>Returned: 57, ip IP_ADDRESS is blacklisted</td>
						</tr>
						<tr>
							<td></td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td></td>
							<td></td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td>66</td>
							<td>ERROR_CREATE_SQLITE3_CONNECTION</td>
							<td>SQL connection could not be made, This can happen if the file cannot be found or created</td>
							<td>Returned: 66, connection to sqlite3 database failed when executing function FTN on table TABLE with message - \"MSG\"</td>
						</tr>
						<tr>
							<td>67</td>
							<td>ERROR_EXECUTE_SQLITE3_COMMAND</td>
							<td>SQL command could not be execute based on input</td>
							<td>Returned: 67, executing command of type TYPE failed on table TABLE with message - \"MSG\"</td>
						</tr>
						<tr>
							<td>68</td>
							<td>ERROR_NO_ID_PROVIDED</td>
							<td>SQL Command requires an id to run and must be passed run again with an id</td>
							<td>Returned: 68, executing command CMD on table TABLE requires ID but no ID was provided</td>
						</tr>
						<tr>
							<td>69</td>
							<td>ERROR_SQL_RETURN_CAST</td>
							<td>SQL select query returns a set of values of which at least one of them could not be casted to the expected type i.e. the return type was unexpected.</td>
							<td>Returned: 69, after executing command CMD there was an error casting an element of returned tuple to TYPE type - \"MSG\"</td>
						</tr>
						<tr>
							<td>70</td>
							<td>ERROR_SQL_RETURN_MISSING_ATTR</td>
							<td>SQL command did not return the number of values expected. Either returned no values as no entry corresponding to given command exists or returns some number of values not equal to the expected number of values.</td>
							<td>Returned: 70, after executing command CMD on table TABLE, only ATTR_GIVEN attributes were returned out of expected ATTR_EXPECTED</td>
						</tr>
					</tbody>
				</table>
			</div>
        );
	}
}

export default ErrorDoc
