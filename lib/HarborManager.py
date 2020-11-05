# -*- coding: utf-8 -*-
from harborclient_light.harborclient import HarborClient
from lib.settings import HARBOR_USER, HARBOR_PASSWORD, HARBOR_URL
from lib.Log import RecodeLog


class HarborManager:
    def __init__(self):
        self.client = None

    def login(self, **kwargs):
        self.client = HarborClient(**kwargs)

    def get_project(self):
        """
        :return:
        """
        if not self.client:
            RecodeLog.error('harbor还没登录')
            raise Exception("harbor还没登录")
        project_list = list()
        for x in self.client.get_projects():
            project_list.append({
                'project_name': x['name'],
                'project_id': x['project_id']
            })
        return project_list

    def get_repo(self, project_id):
        repo_list = list()
        for y in self.client.get_repositories(project_id=project_id):
            repo_list.append({
                'repo_name': y['name'],
                'tags_count': y['tags_count'],
                'creation_time': y['creation_time']
            })
        return repo_list

    def get_remove_repo(self, save_count=4):
        """
        :param save_count:
        :return:
        """
        projects = self.get_project()
        if not projects:
            RecodeLog.error('没有获取到项目列表!')
            raise Exception("没有获取到项目列表！")
        for project in projects:
            for v in self.get_repo(project_id=project['project_id']):
                if v['tags_count'] <= save_count:
                    continue
                if not v['repo_name'].startswith('images'):
                    continue
                self.get_remove_tags(
                    repo_name=v['repo_name'],
                    remove_count=int(v['tags_count']) - save_count
                )

    def get_remove_tags(self, repo_name, remove_count):
        """
        :param repo_name:
        :param remove_count:
        :return:
        """
        tags = self.client.get_repository_tags(repo_name=repo_name)
        health = sorted(tags, key=lambda k: k['created'])
        health = [{'tag': x['name'], 'repo_name': repo_name, 'created': x['created']} for x in health]
        RecodeLog.info("repo:{1}的完整tag列表为:{0}".format(health, repo_name))
        RecodeLog.info("开始删除repo:{0}的相关tag,删除tag个数为:{1}".format(repo_name, remove_count))
        for tag in health[0:remove_count]:
            result = self.client.delete_repository_tag(repo_name=tag['repo_name'], tag=tag['tag'])
            if result:
                RecodeLog.info(msg="删除镜像:{0},tag:{1},成功！".format(tag['repo_name'], tag['tag']))
            else:
                RecodeLog.info(msg="删除镜像:{0},tag:{1},失败！原因：{2}".format(tag['repo_name'], tag['tag'], result))


def run():
    h = HarborManager()
    h.login(user=HARBOR_USER, password=HARBOR_PASSWORD, host=HARBOR_URL)
    # h.get_project()
    h.get_remove_repo()
    # h.get_tags(repo_name='malltest/mall-task')
