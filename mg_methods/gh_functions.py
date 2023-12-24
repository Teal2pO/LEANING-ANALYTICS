from github import Github
import json


class tealGitHub:
    def __init__(self):
        self = []

    def get_GitHub_user(self, gToken):
        g = Github(gToken)
        return g

    def get_GitHub_organization_repos(self, gToken, gUser):
        response = []
        status = 'error'
        try:
            g = Github(gToken)
            self.organization = g.get_organization(gUser)
            response = [{"label": repo.name, "value": ir}
                        for ir, repo in enumerate(self.organization.get_repos())]
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def get_repo_info(self, gToken, gUser, reponame):
        response = []
        status = 'error'
        try:
            g = Github(gToken)
            fileNames = []
            repo = g.get_repo(gUser+'/'+reponame)
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
            response = {'branch_names': branchNames, 'file_names': fileNames}
            status = 'success'
        except:
            pass

        return {'status': status, 'response': response}

    def get_repo_file_content(self, gToken, gUser, reponame, branchname, filename):
        response = []
        status = 'error'
        try:
            g = Github(gToken)
            repo = g.get_repo(gUser+'/'+reponame)
            b = repo.get_branch(branch=branchname)
            contents = repo.get_contents(filename, ref=b.commit.sha)
            # self.contents = self.repo.get_file_contents(filename, ref=b.commit.sha)
            response = {'repo': repo, 'contents': contents}
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def get_GitHub_repo_content(self, gToken, gUser, reponame, branchname):
        response = []
        status = 'success'
        try:
            repoFiles = self.get_repo_info(gToken, gUser, reponame)['response']
            # print(repoFiles)
            outDict = {}
            for filename in repoFiles['file_names']:
                # print(filename)
                # print(self.get_repo_file_content(gToken,gUser,reponame,branchname,filename))
                outDict[filename] = json.loads(str(self.get_repo_file_content(gToken, gUser, reponame, branchname, filename)[
                                               'response']['contents'].decoded_content, encoding="ascii", errors='strict'))
            response = outDict
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def write_file_2_repo(self, gToken, gUser, reponame, branchname, filename, comment, content):
        response = []
        status = 'success'
        try:
            g = Github(gToken)
            repo = g.get_repo(gUser+'/'+reponame)
            repo.create_file(filename, comment, content, branch=branchname)
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def delete_file(self, gToken, gUser, reponame, branchname, filename):
        response = []
        status = 'error'
        try:
            g = Github(gToken)
            repoName = reponame
            branchName = branchname
            repo = g.get_repo(gUser+'/'+reponame)
            b = repo.get_branch(branch=branchname)
            contents = repo.get_contents(filename, ref=b.commit.sha)
            repo.delete_file(
                contents.path, params['commitComment'], contents.sha, branch=branchname)
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def delete_repo(self, gToken, gUser, reponame):
        response = []
        status = 'error'
        try:
            g = Github(gToken)
            repoName = reponame
            repo = g.get_repo(gUser+'/'+reponame)
            repo.delete()
            status = 'success'
        except:
            pass
        return {'status': status, 'response': response}

    def create_branch(self, gToken, gUser, reponame, sourcebranch, targetbranch):
        response = []
        status = 'success'
        try:
            g = Github(gUser, gToken)
            repo = g.get_repo(gUser+'/'+reponame)
            sb = repo.get_branch(sourcebranch)
            response0 = repo.create_git_ref(
                ref='refs/heads/' + targetbranch, sha=sb.commit.sha)
            response = response0.ref
        except:
            pass
        return {'status': status, 'response': response}

    def create_update_repos(self, gToken, gUser, reponame, branchname, filename, content, comment):
        response = []
        status = 'error'
        reposList = [dct['label'] for dct in self.get_GitHub_organization_repos(gToken, gUser)[
            'response']]
        if reponame in reposList:
            try:
                fileOut = self.get_repo_file_content(
                    gToken, gUser, reponame, filename)
                contentExist = fileOut['contents']
                repo = fileOut['repo']
                repo.update_file(content.path, comment, content,
                                 contentExist.sha, branch=branchname)
                status = 'Content updated'
            except:
                self.write_file_2_repo(
                    gToken, gUser, reponame, branchname, filename, comment, content)
                status = 'Content created'

        else:
            self.organization.create_repo(reponame, private=True)
            self.write_file_2_repo(
                gToken, gUser, reponame, branchname, filename, comment, content)
            status = 'Content created'
        return {'status': status, 'response': response}

    def create_bracnch_or_repo(self, gToken, gUser, reponame, mainbranch, newbranch, filename, content, comment):
        response = []
        status = 'error'
        reposList = [dct['label'] for dct in self.get_GitHub_organization_repos(gToken, gUser)[
            'response']]
        if reponame in reposList:
            try:
                temp = create_branch(self, gToken, gUser,
                                     reponame, mainbranch, newbranch)
                self.write_file_2_repo(
                    gToken, gUser, reponame, newbranch, filename, comment, content)
                status = temp['response']
            except:
                status = 'branch not created'
        else:
            self.organization.create_repo(reponame, private=True)
            self.write_file_2_repo(
                gToken, gUser, reponame, 'main', filename, comment, content)
            status = 'repo with branch main created'
        return {'status': status, 'response': response}
