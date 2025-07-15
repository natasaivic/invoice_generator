document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('invoiceForm');
    const addItemBtn = document.getElementById('add-item');
    const itemsList = document.getElementById('items-list');
    const totalAmount = document.getElementById('total-amount');
    const previewBtn = document.getElementById('preview-btn');
    const previewSection = document.getElementById('preview-section');
    const invoicePreview = document.getElementById('invoice-preview');

    let itemCount = 0;

    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    
    // Set default due date to 30 days from today
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + 30);
    document.getElementById('due_date').value = dueDate.toISOString().split('T')[0];

    // Generate default invoice number
    const invoiceNumber = 'INV-' + Date.now().toString().slice(-6);
    document.getElementById('invoice_number').value = invoiceNumber;

    // Add initial item row
    addItem();

    // Add item functionality
    addItemBtn.addEventListener('click', addItem);

    function addItem() {
        itemCount++;
        const itemRow = document.createElement('div');
        itemRow.className = 'item-row';
        itemRow.innerHTML = `
            <input type="text" name="description_${itemCount}" placeholder="Description" required>
            <input type="number" name="quantity_${itemCount}" placeholder="Qty" min="0" step="0.01" value="1" required>
            <input type="number" name="rate_${itemCount}" placeholder="Rate" min="0" step="0.01" required>
            <span class="amount">$0.00</span>
            <button type="button" class="btn btn-danger remove-item">Remove</button>
        `;
        
        itemsList.appendChild(itemRow);

        // Add event listeners for calculations
        const quantityInput = itemRow.querySelector('input[name^="quantity_"]');
        const rateInput = itemRow.querySelector('input[name^="rate_"]');
        const removeBtn = itemRow.querySelector('.remove-item');

        quantityInput.addEventListener('input', calculateRowAmount);
        rateInput.addEventListener('input', calculateRowAmount);
        removeBtn.addEventListener('click', function() {
            itemRow.remove();
            calculateTotal();
        });

        function calculateRowAmount() {
            const quantity = parseFloat(quantityInput.value) || 0;
            const rate = parseFloat(rateInput.value) || 0;
            const amount = quantity * rate;
            itemRow.querySelector('.amount').textContent = `$${amount.toFixed(2)}`;
            calculateTotal();
        }
    }

    function calculateTotal() {
        const amounts = document.querySelectorAll('.amount');
        let total = 0;
        amounts.forEach(amount => {
            const value = parseFloat(amount.textContent.replace('$', '')) || 0;
            total += value;
        });
        totalAmount.textContent = total.toFixed(2);
    }

    // Preview functionality
    previewBtn.addEventListener('click', generatePreview);

    function generatePreview() {
        const formData = new FormData(form);
        const data = {};
        
        // Get form data
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Get items data
        const items = [];
        const itemRows = document.querySelectorAll('.item-row');
        itemRows.forEach((row, index) => {
            const description = row.querySelector('input[name^="description_"]').value;
            const quantity = row.querySelector('input[name^="quantity_"]').value;
            const rate = row.querySelector('input[name^="rate_"]').value;
            
            if (description && quantity && rate) {
                items.push({
                    description: description,
                    quantity: parseFloat(quantity),
                    rate: parseFloat(rate)
                });
            }
        });

        // Generate preview HTML
        const previewHTML = generatePreviewHTML(data, items);
        invoicePreview.innerHTML = previewHTML;
        previewSection.style.display = 'block';
        previewSection.scrollIntoView({ behavior: 'smooth' });
    }

    function generatePreviewHTML(data, items) {
        let total = 0;
        const itemsHTML = items.map(item => {
            const amount = item.quantity * item.rate;
            total += amount;
            return `
                <tr>
                    <td>${item.description}</td>
                    <td>${item.quantity}</td>
                    <td>$${item.rate.toFixed(2)}</td>
                    <td class="amount-col">$${amount.toFixed(2)}</td>
                </tr>
            `;
        }).join('');

        return `
            <h1>INVOICE</h1>
            
            <div class="invoice-header">
                <div class="invoice-from">
                    <h3>FROM:</h3>
                    <div>${data.from_name || ''}</div>
                    <div>${data.from_company || ''}</div>
                    <div>${data.from_address || ''}</div>
                    <div>${data.from_city || ''}</div>
                    <div>${data.from_email || ''}</div>
                    <div>${data.from_phone || ''}</div>
                </div>
                
                <div class="invoice-to">
                    <h3>TO:</h3>
                    <div>${data.to_name || ''}</div>
                    <div>${data.to_company || ''}</div>
                    <div>${data.to_address || ''}</div>
                    <div>${data.to_city || ''}</div>
                    <div>${data.to_email || ''}</div>
                </div>
            </div>

            <div class="invoice-details">
                <div><strong>Invoice #:</strong> ${data.invoice_number || ''}</div>
                <div><strong>Date:</strong> ${data.date || ''}</div>
                <div><strong>Due Date:</strong> ${data.due_date || ''}</div>
            </div>

            <div class="invoice-items">
                <table>
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th>Quantity</th>
                            <th>Rate</th>
                            <th class="amount-col">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemsHTML}
                    </tbody>
                </table>
            </div>

            <div class="invoice-total">
                Total: $${total.toFixed(2)}
            </div>

            ${data.notes ? `
                <div class="invoice-notes">
                    <h4>Notes:</h4>
                    <p>${data.notes}</p>
                </div>
            ` : ''}
        `;
    }

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {};
        
        // Get form data
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Get items data
        const items = [];
        const itemRows = document.querySelectorAll('.item-row');
        itemRows.forEach((row, index) => {
            const description = row.querySelector('input[name^="description_"]').value;
            const quantity = row.querySelector('input[name^="quantity_"]').value;
            const rate = row.querySelector('input[name^="rate_"]').value;
            
            if (description && quantity && rate) {
                items.push({
                    description: description,
                    quantity: parseFloat(quantity),
                    rate: parseFloat(rate)
                });
            }
        });

        data.items = items;

        // Send to server
        fetch('/generate_invoice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Network response was not ok');
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `invoice_${data.invoice_number}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating invoice. Please try again.');
        });
    });
});