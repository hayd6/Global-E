/** @type {import('next').NextConfig} */
const isGithubActions = process.env.GITHUB_ACTIONS || false;
let repo = '';
if (isGithubActions) {
  const repoName = process.env.GITHUB_REPOSITORY ? process.env.GITHUB_REPOSITORY.split('/')[1] : '';
  repo = repoName ? `/${repoName}` : '';
}

const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  basePath: isGithubActions ? repo : '',
};

module.exports = nextConfig;

