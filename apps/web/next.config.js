/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  images: {
    domains: ['localhost'],
  },
  transpilePackages: [
    '@radix-ui/react-label',
    '@radix-ui/react-slot',
    '@radix-ui/react-dialog',
    '@radix-ui/react-select',
    '@radix-ui/react-toast',
    '@radix-ui/react-dropdown-menu',
  ],
  webpack: (config) => {
    config.resolve.modules = [__dirname, 'node_modules', '../../node_modules'];
    return config;
  },
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/:path*`,
      },
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

module.exports = nextConfig;

