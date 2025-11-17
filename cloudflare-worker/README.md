# Cloudflare Worker Setup - Shopee API Proxy

## Problem
Shopee blocks direct API requests from servers with **403 Forbidden** error, preventing real-time product fetching.

## Solution
Use **Cloudflare Worker** as a proxy to fetch Shopee data without being blocked.

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Deploy Cloudflare Worker

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click **Workers & Pages** → **Create Worker**
3. Name it: `shopee-proxy` (or any name)
4. Click **Deploy**
5. Click **Edit Code**
6. **Delete** the default code
7. **Copy & Paste** the code from `cloudflare-worker/shopee-proxy.js`
8. Click **Deploy**
9. Copy your Worker URL (e.g., `https://shopee-proxy.your-account.workers.dev`)

### Step 2: Configure Django

Add to Vercel Environment Variables:

```
SHOPEE_PROXY=https://your-worker-url.workers.dev
SHOPEE_SHOP_ID=53252649
```

**In Vercel Dashboard:**
1. Go to Project → Settings → Environment Variables
2. Add `SHOPEE_PROXY` = your Cloudflare Worker URL
3. Add `SHOPEE_SHOP_ID` = `53252649`
4. Redeploy

### Step 3: Test

Visit your website:
- Homepage: `/`
- Products: `/products/`

✅ Products should load without 403 errors!

---

## 📋 How It Works

```
Django (Vercel) → Cloudflare Worker → Shopee API
                   ↑ Browser headers
                   ↑ No 403 block!
```

1. **Django** requests: `https://your-worker.workers.dev/?shopid=53252649&limit=50`
2. **Worker** fetches Shopee with browser headers
3. **Shopee** returns data (thinks it's a browser)
4. **Worker** sends data back to Django
5. **Django** renders products

---

## 🛠️ Configuration

### Environment Variables

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `SHOPEE_PROXY` | **Yes** | `https://shopee-proxy.workers.dev` | Cloudflare Worker URL |
| `SHOPEE_SHOP_ID` | **Yes** | `53252649` | Your Shopee shop ID |
| `INSTAGRAM_ACCESS_TOKEN` | No | `IGQWRPxxx...` | Instagram API token |

### Get Shop ID

Visit your Shopee store and check the URL:
```
https://shopee.co.id/shop/53252649/   ← This is your shop ID
```

Or Django will auto-resolve from username `modelmanis34`.

---

## 🔧 Troubleshooting

### Worker not working?

**Check Worker URL:**
```bash
curl "https://your-worker.workers.dev/?shopid=53252649"
```

Should return JSON with products.

**Check Django logs:**
```
Using Cloudflare Worker Proxy for Shopee API  ← Good!
SHOPEE_PROXY not configured  ← Bad! Add env var
```

### Still getting 403?

- ✅ Verify Worker is deployed
- ✅ Verify `SHOPEE_PROXY` env var in Vercel
- ✅ Redeploy Vercel after adding env var
- ✅ Check Worker code matches `shopee-proxy.js`

### No products showing?

1. Check if fallback notice appears: "Produk tidak dapat dimuat"
2. Check Vercel logs for errors
3. Verify shop ID is correct

---

## 📦 Fallback Behavior

If Worker fails or is not configured:
- Shows 3 placeholder products
- Displays notice: "Produk tidak dapat dimuat, silakan kunjungi toko Shopee kami"
- All products link to `https://shopee.co.id/modelmanis34`

---

## 🎯 Worker Features

- ✅ **No 403 blocks** - Browser-like headers
- ✅ **Fast** - Cloudflare edge network
- ✅ **Cached** - 10 minutes cache
- ✅ **CORS enabled** - Works from any domain
- ✅ **Free tier** - 100,000 requests/day

---

## 📝 Manual Product Update (Alternative)

If you don't want to use Worker, manually update `get_static_products()` in `Blog/posting/utils/shopee_api.py`:

```python
def get_static_products():
    return [
        {
            'name': 'Your Product Name',
            'price': 150000,
            'image': 'https://cf.shopee.co.id/file/YOUR_IMAGE_ID',
            'url': settings.SHOPEE_STORE_URL,
            # ... other fields
        },
        # Add more products...
    ]
```

Update monthly or weekly with real data from your Shopee store.

---

## 🔐 Security Notes

- Worker is public (anyone can use it)
- No authentication required
- Only reads public Shopee data
- No login/password needed
- Safe for production

---

## 💡 Why Cloudflare Worker?

| Direct API | With Worker |
|------------|-------------|
| ❌ 403 Forbidden | ✅ Works perfectly |
| ❌ Blocked by Shopee | ✅ Browser-like headers |
| ❌ Unreliable | ✅ 99.9% uptime |
| ❌ Slow from Vercel | ✅ Fast from CF edge |

---

## 📞 Support

If you need help:
1. Check Vercel deployment logs
2. Check Cloudflare Worker logs
3. Verify environment variables
4. Test Worker URL directly with curl

**Common Issues:**
- Forgot to add `SHOPEE_PROXY` env var → Add in Vercel settings
- Worker URL wrong → Copy exact URL from CF dashboard
- Shop ID wrong → Check Shopee store URL

---

## 🎉 Success Checklist

- [ ] Cloudflare Worker deployed
- [ ] Worker URL added to Vercel env vars
- [ ] Shop ID configured (53252649)
- [ ] Vercel redeployed
- [ ] Products showing on website
- [ ] No 403 errors in logs

**Deployment successful! 🚀**
