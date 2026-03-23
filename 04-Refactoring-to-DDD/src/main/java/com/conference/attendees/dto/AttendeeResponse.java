package com.conference.attendees.dto;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * Data Transfer Object for attendee responses.
 * Used for REST API output.
 */
public class AttendeeResponse implements Serializable {

    private Long id;
    private String email;
    private String firstName;
    private String lastName;
    private String fullName;
    private String streetAddress;
    private String bus;
    private String postalCode;
    private String townOrMunicipality;
    private LocalDateTime registrationDate;
    private String status;

    public AttendeeResponse() {}

    public AttendeeResponse(Long id, String email, String firstName, String lastName,
                          String streetAddress, String bus, String postalCode,
                          String townOrMunicipality, LocalDateTime registrationDate,
                          String status) {
        this.id = id;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.fullName = firstName + " " + lastName;
        this.streetAddress = streetAddress;
        this.bus = bus;
        this.postalCode = postalCode;
        this.townOrMunicipality = townOrMunicipality;
        this.registrationDate = registrationDate;
        this.status = status;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

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

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
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

    public LocalDateTime getRegistrationDate() {
        return registrationDate;
    }

    public void setRegistrationDate(LocalDateTime registrationDate) {
        this.registrationDate = registrationDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "AttendeeResponse{" +
                "id=" + id +
                ", email='" + email + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", fullName='" + fullName + '\'' +
                ", streetAddress='" + streetAddress + '\'' +
                ", bus='" + bus + '\'' +
                ", postalCode='" + postalCode + '\'' +
                ", townOrMunicipality='" + townOrMunicipality + '\'' +
                ", registrationDate=" + registrationDate +
                ", status='" + status + '\'' +
                '}';
    }
}