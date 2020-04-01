import CocoaMQTT
import UIKit

class ViewController: UIViewController {
    
    // CocoaMQTT client and server sensing + switch function
    
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host: "192.168.1.16", port: 1883)
    
    @IBAction func connectmsqtt(_: UIButton) {
        mqttClient.connect()
    }

    @IBAction func disconnectmqtt(_: UIButton) {
        mqttClient.disconnect()
    }
    
    @IBAction func solenoidvalve(_ sender: UISwitch) {
        if sender.isOn {
            mqttClient.publish("rpi/gpio", withString: "on")
        } else {
            mqttClient.publish("rpi/gpio", withString: "off")
        }
    }
    
    // UIDatePicker as input for UITextField
    
    @IBOutlet var inputTextField: UITextField!
    
    private var datePicker: UIDatePicker?
    
    @objc func dateChanged(datePicker: UIDatePicker) {
        let dateFormatter = DateFormatter()
        dateFormatter.timeStyle = .short
        inputTextField.text = dateFormatter.string(from: datePicker.date)
        view.endEditing(true)
    }
    
    @objc func viewTapped(gestureRecognizer _: UITapGestureRecognizer) {
         view.endEditing(true)
     }

    // config button function
    
    @IBAction func Config(_ sender: UIButton) {
        
        if sender.isEnabled {
            let text: String = inputTextField.text!
            datePicker?.addTarget(self, action: #selector(dateChanged(datePicker:)), for: .valueChanged)
            mqttClient.publish("rpi/gpio", withString: text)
            
        }
    }

    // view did load
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        datePicker = UIDatePicker()
        datePicker?.datePickerMode = .time
        inputTextField.inputView = datePicker
        datePicker?.addTarget(self, action: #selector(dateChanged(datePicker:)), for: .valueChanged)

        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(ViewController.viewTapped(gestureRecognizer:)))
        view.addGestureRecognizer(tapGesture)
    
        // Do any additional setup after loading the view.
    }

}
