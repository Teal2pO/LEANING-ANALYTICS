from github import Github


class tealGitHub:
    def __init__(self):
        self = []

    def get_GitHub_user(self, params):
        g = Github(params['gToken'])
        return g

    def get_GitHub_organization_repos(self, params):
        g = Github(params['gToken'])
        self.organization = g.get_organization(params['gUser'])
        repoNames = [repo.name for repo in self.organization.get_repos()]
        return {'reponames': repoNames}

    def get_repo_info(self, params):
        g = Github(params['gToken'])
        fileNames = []
        repoName = params['repoName']
        repo = g.get_repo(params['gUser']+'/'+params['repoName'])
        branches = list(repo.get_branches())
        branchNames = [br.name for br in branches]
        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                fls = repo.get_contents(file_content.path)
                contents.extend(fls)
            else:
                fileNames += [file_content.path]

        return {'branch_names': branchNames, 'file_names': fileNames}

    def get_repo_file_content(self, params):
        g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        # self.contents = self.repo.get_file_contents(params['fileName'], ref=b.commit.sha)
        return {'repo': repo, 'contents': contents}

    def write_file_2_repo(self, params):
        g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = g.get_repo(params['gUser']+'/'+params['repoName'])
        repo.create_file(params['writeFile'], params['commitComment'],
                         params['content2Write'], branch=params['branchName'])
        return {'status': 'success'}

    def delete_file(self, params):
        g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        repo.delete_file(
            contents.path, params['commitComment'], contents.sha, branch=params['branchName'])
        return {'status': 'success'}

    def delete_repo(self, params):
        g = Github(params['gToken'])
        repoName = params['repoName']
        repo = g.get_repo(params['gUser']+'/'+params['repoName'])
        repo.delete()
        return {'status': 'success'}

    def create_update_GITHUB_organization_repos(self, parameters):
        functionParameters = {'gToken': parameters['access_parameters']['gToken'], 'gUser': parameters['access_parameters']['gUser'], 'repoName': parameters['repoName'],
                              'branchName': 'main', 'writeFile': parameters['fileInfoDict']['filename'], 'content2Write': parameters['fileInfoDict']['filecontent'], 'commitComment': parameters['updateComment']}
        inputDict = parameters['access_parameters']
        reposList = self.get_GitHub_organization_repos(inputDict)['reponames']
        if parameters['repoName'] in reposList:
            functionParameters['fileName'] = parameters['fileInfoDict']['filename']
            inputDict = functionParameters
            try:
                fileOut = self.get_repo_file_content(inputDict)
                content = fileOut['contents']
                repo = fileOut['repo']
                repo.update_file(
                    content.path, parameters['updateComment'], parameters['fileInfoDict']['filecontent'], content.sha, branch='main')
                message = 'Content updated'
            except:
                inputDictWrite = functionParameters
                self.write_file_2_repo(inputDictWrite)
                message = 'Content created'

        else:
            self.organization.create_repo(parameters['repoName'], private=True)
            inputDictWrite = functionParameters
            self.write_file_2_repo(inputDictWrite)
            message = 'Content created'
        return {'status': message}

    def get_GitHub_repo_content(self, paramsInfo):
        repoFiles = self.get_repo_info(paramsInfo)
        print(repoFiles)
        params = {'gToken': paramsInfo['gToken'], 'gUser': paramsInfo['gUser'],
                  'branchName': repoFiles['branch_names'][0], 'repoName': paramsInfo['repoName'], 'fileName': ''}
        outDict = {}
        for file in repoFiles['file_names']:
            params['fileName'] = file
            outDict[file] = json.loads(str(self.get_repo_file_content(
                params)['contents'].decoded_content, encoding="ascii", errors='strict'))
        return outDict

    def get_GitHub_repo_content_string(self, paramsInfo):
        repoFiles = self.get_repo_info(paramsInfo)
        print(repoFiles)
        params = {'gToken': paramsInfo['gToken'], 'gUser': paramsInfo['gUser'],
                  'branchName': repoFiles['branch_names'][0], 'repoName': paramsInfo['repoName'], 'fileName': ''}
        outDict = {}
        for file in repoFiles['file_names']:
            params['fileName'] = file
            outDict[file] = str(self.get_repo_file_content(
                params)['contents'].decoded_content, encoding="ascii", errors='strict')
        return outDict
