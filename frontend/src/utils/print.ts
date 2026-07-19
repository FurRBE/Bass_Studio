import type { OrderDetail } from '@/types'

const CATEGORY_LABELS: Record<string, string> = {
  body: '琴体木材',
  neck: '琴颈木材',
  fingerboard: '指板材质',
  pickup: '拾音器',
  bridge: '琴桥',
  finish: '颜色/漆面',
  strings: '弦数',
  handedness: '左右手',
}

const STATUS_LABELS: Record<string, string> = {
  pending: '待确认',
  confirmed: '已确认',
  production: '制作中',
  completed: '已完成',
  cancelled: '已取消',
}

export function printOrder(order: OrderDetail) {
  const orderId = `#${String(order.id).padStart(6, '0')}`
  const createdAt = formatPrintDate(order.created_at)
  const status = STATUS_LABELS[order.status] || order.status
  const addr = order.shipping_address

  const configRows = (order.configuration || [])
    .map(
      (item) => `
    <tr>
      <td>${CATEGORY_LABELS[item.category] || item.category}</td>
      <td>${item.name}</td>
      <td style="text-align:right;">${item.price > 0 ? '¥' + item.price.toLocaleString() : '已包含'}</td>
    </tr>`,
    )
    .join('')

  const shippingHtml = addr
    ? `
    <div class="section">
      <h3>收货信息</h3>
      <p><strong>收件人：</strong>${escapeHtml(addr.recipient_name)} <strong>电话：</strong>${escapeHtml(addr.recipient_phone)}</p>
      <p><strong>地址：</strong>${escapeHtml(addr.address_line1)} ${escapeHtml(addr.address_line2)}，${escapeHtml(addr.city)} ${escapeHtml(addr.state)} ${escapeHtml(addr.zip_code)}</p>
      ${addr.notes ? `<p><strong>备注：</strong>${escapeHtml(addr.notes)}</p>` : ''}
    </div>`
    : ''

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>订单 ${orderId} - 打印</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
      color: #222;
      background: #fff;
      padding: 40px;
      max-width: 800px;
      margin: 0 auto;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 2px solid #1F6B4F;
    }
    .header h1 {
      font-size: 24px;
      letter-spacing: 4px;
      color: #1F6B4F;
      margin-bottom: 4px;
    }
    .header .subtitle {
      font-size: 13px;
      color: #888;
    }
    .order-meta {
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
      font-size: 14px;
    }
    .order-meta .left span { margin-right: 24px; }
    .order-meta .right { font-weight: 600; color: #1F6B4F; }
    .section {
      margin-bottom: 24px;
    }
    .section h3 {
      font-size: 15px;
      margin-bottom: 10px;
      color: #333;
      border-left: 3px solid #1F6B4F;
      padding-left: 10px;
    }
    .section p {
      font-size: 13px;
      color: #555;
      margin-bottom: 4px;
      line-height: 1.6;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid #eaeaea;
    }
    th {
      background: #f8f8f8;
      color: #666;
      font-weight: 500;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .total-row td {
      font-weight: 700;
      font-size: 15px;
      border-top: 2px solid #1F6B4F;
      padding-top: 12px;
    }
    .footer {
      text-align: center;
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #eaeaea;
      font-size: 12px;
      color: #aaa;
    }
    .status-badge {
      display: inline-block;
      padding: 3px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: #fff;
      background: #1F6B4F;
    }
    @media print {
      body { padding: 20px; }
      @page { margin: 15mm; }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>🎸 BASS STUDIO</h1>
    <div class="subtitle">贝斯定制工作室 · 订单确认单</div>
  </div>

  <div class="order-meta">
    <div class="left">
      <span><strong>订单编号：</strong>${orderId}</span>
      <span><strong>下单时间：</strong>${createdAt}</span>
    </div>
    <div class="right">
      <span class="status-badge">${status}</span>
    </div>
  </div>

  ${shippingHtml}

  <div class="section">
    <h3>配置明细</h3>
    <table>
      <thead>
        <tr>
          <th style="width:25%;">分类</th>
          <th style="width:50%;">选项</th>
          <th style="width:25%;text-align:right;">价格</th>
        </tr>
      </thead>
      <tbody>
        ${configRows}
        <tr class="total-row">
          <td colspan="2" style="text-align:right;">总计</td>
          <td style="text-align:right;">¥${order.total_price.toLocaleString()}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="footer">
    <p>感谢您选择 Bass Studio 定制贝斯！</p>
    <p>如有任何疑问，请联系客服。</p>
  </div>

  <script>
    window.onload = () => { window.print(); };<` + `/script>
</body>
</html>`

  const printWindow = window.open('', '_blank', 'width=800,height=600')
  if (printWindow) {
    printWindow.document.write(html)
    printWindow.document.close()
  }
}

function formatPrintDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function escapeHtml(str: string) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
