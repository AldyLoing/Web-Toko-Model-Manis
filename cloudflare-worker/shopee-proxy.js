/**
 * Cloudflare Worker - Shopee API Proxy
 * 
 * Deploy instructions:
 * 1. Go to https://dash.cloudflare.com
 * 2. Workers & Pages -> Create Worker
 * 3. Paste this code
 * 4. Deploy
 * 5. Copy worker URL (e.g., https://shopee-proxy.your-account.workers.dev)
 * 6. Add to Django .env: SHOPEE_PROXY=https://your-worker-url.workers.dev
 */

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    const url = new URL(request.url);
    const shopId = url.searchParams.get("shopid");
    const limit = url.searchParams.get("limit") || "50";
    const offset = url.searchParams.get("offset") || "0";

    if (!shopId) {
      return new Response(
        JSON.stringify({ error: "Missing shopid parameter" }),
        {
          status: 400,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
    }

    // Build Shopee API URL
    const shopeeUrl = `https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=${limit}&match_id=${shopId}&newest=${offset}&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2`;

    try {
      // Fetch from Shopee with complete browser-like headers
      const response = await fetch(shopeeUrl, {
        method: "GET",
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
          "Accept": "*/*",
          "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
          "Accept-Encoding": "gzip, deflate, br",
          "Referer": "https://shopee.co.id/",
          "Origin": "https://shopee.co.id",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="122", "Chromium";v="122"',
          "Sec-Ch-Ua-Mobile": "?0",
          "Sec-Ch-Ua-Platform": '"Windows"',
          "X-Requested-With": "XMLHttpRequest",
          "X-Api-Source": "pc",
        },
      });

      // Get response data
      const data = await response.json();

      // Return with CORS headers
      return new Response(JSON.stringify(data), {
        status: response.status,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "public, max-age=600", // Cache 10 minutes
        },
      });
    } catch (error) {
      return new Response(
        JSON.stringify({
          error: "Failed to fetch from Shopee",
          message: error.message,
        }),
        {
          status: 500,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
    }
  },
};
