## Bitbucket Pull Request Manager

### Overview

You can use this python script to easily track the state of any pull requests which may be open for your current branch inside a git repository.
Note, this only works with BitBucket.

### Example output

```
BitBucket username:
$<>
BitBucket password:
$<>

	REMOTE
		ssh://git@REMOTE_BACKEND/SLUG/PROJECT.git

	BRANCH
		YOUR_BRANCH_NAME

	PULL REQUEST
		https://REMOTE_BACKEND/projects/SLUG/repos/PROJECT/pull-requests/618/overview


	NEEDS WORK


	APPROVALS
		User: User_One
		Time: 2020-03-17 13:27:38.880000

		User: User_Two
		Time: 2020-03-17 12:39:33.424000
		
	        User: User_Three
		Time: 2020-03-17 12:12:10.129000


	COMMENTS
		User: User_One
		Time: 2020-03-17 11:23:44.641000
		File: N/A
		Comment: I think you should change the url


		User: User_Two
		Time: 2020-03-17 12:13:56.141000
		File: N/A
		Comment: Looks good to me! :)


		User: User_Three
		Time: 2020-03-17 12:12:45.062000
		File: package.json:85
		Comment: I don't think we need this dependency!



```
