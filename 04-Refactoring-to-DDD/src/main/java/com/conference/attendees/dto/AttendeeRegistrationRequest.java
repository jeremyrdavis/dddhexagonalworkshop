package com.conference.attendees.dto;

import java.io.Serializable;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/**
 * Data Transfer Object for attendee registration requests.
 * Used for REST API input.
 */
public class AttendeeRegistrationRequest implements Serializable {

    @Email(message = "Email should be valid")
    @NotBlank(message = "Email is required")
    private String email;

    @NotBlank(message = "First name is required")
    private String firstName;

    @NotBlank(message = "Last name is required")
    private String lastName;

    @NotBlank(message = "Street address is required")
    private String streetAddress;

    private String bus;

    @NotBlank(message = "Postal code is required")
    private String postalCode;

    @NotBlank(message = "Town or municipality is required")
    private String townOrMunicipality;

    public AttendeeRegistrationRequest() {}

    public AttendeeRegistrationRequest(String email, String firstName, String lastName,
                                     String streetAddress, String bus, String postalCode,
                                     String townOrMunicipality) {
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.streetAddress = streetAddress;
        this.bus = bus;
        this.postalCode = postalCode;
        this.townOrMunicipality = townOrMunicipality;
    }

    // Getters and Setters
    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getStreetAddress() {
        return streetAddress;
    }

    public void setStreetAddress(String streetAddress) {
        this.streetAddress = streetAddress;
    }

    public String getBus() {
        return bus;
    }

    public void setBus(String bus) {
        this.bus = bus;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    public String getTownOrMunicipality() {
        return townOrMunicipality;
    }

    public void setTownOrMunicipality(String townOrMunicipality) {
        this.townOrMunicipality = townOrMunicipality;
    }

    @Override
    public String toString() {
        return "AttendeeRegistrationRequest{" +
                "email='" + email + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", streetAddress='" + streetAddress + '\'' +
                ", bus='" + bus + '\'' +
                ", postalCode='" + postalCode + '\'' +
                ", townOrMunicipality='" + townOrMunicipality + '\'' +
                '}';
    }
}